"""
TODO:
Exceptions file
"""

import argparse
import logging
import sys
import os
import shutil
from colorama import Fore, Style
from .commands import config_parser, aws, TEMPLATES


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="""List EC2 VMs HTML format.\nhttps://github.com/wvoliveira/awslist""")
    parser.add_argument('--region', default='sa-east-1', metavar='\b', help='region', required=False)
    parser.add_argument('--credentials', default='~/.aws/credentials', metavar='\b', help='credentials', required=False)
    parser.add_argument('directory')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
    logging.info('[*] Creating project structure...')

    while True:
        try:
            if os.path.exists(args.directory):
                args.directory = input('{0}[!]{1} This folder already exists.\n'
                                       '{2}[?]{1} Please, choose another:\n> '.format(Fore.RED, Fore.RESET, Fore.YELLOW))
            else:
                break
        except KeyboardInterrupt:
            print('Bye')
            exit(1)

    project_dir = '{}/{}'.format(os.path.abspath('.'), args.directory)
    package_dir = sys.modules['awslist'].__path__[0]

    logging.info('[+] Project directory: {0}{1}{2}'.format(Style.BRIGHT, project_dir, Style.NORMAL))
    src_static_files = os.path.join(package_dir, 'data')
    dst_static_files = os.path.join(project_dir, 'static')
    src_files = os.listdir(src_static_files)

    logging.info('[*] Copying files into the project directory..')
    for dir_name in src_files:
        full_path = os.path.join(src_static_files, dir_name)
        static_path = os.path.join(dst_static_files, dir_name)
        shutil.copytree(full_path, static_path)

    logging.info('[*] Collecting AWS credentials..')
    if '~/.aws/credentials' in args.credentials:
        args.credentials = os.path.join(os.path.expanduser("~"), '.aws/credentials')

    if os.path.exists(args.credentials):
        aws_args = config_parser(args.credentials, 'default')
    else:
        logging.error("{0}[!]{1} File {2}{3}{4} doesnt exists!".format(Fore.RED, Fore.RESET, Style.BRIGHT, args.credentials, Style.NORMAL))
        exit(1)

    region = args.region
    key_id = aws_args['aws_access_key_id']
    access_key = aws_args['aws_secret_access_key']

    logging.info('[*] Trying to connect to AWS..')
    aws_conn = aws.AWS(region, key_id, access_key, '')

    logging.info('[*] Collecting information from AWS..')
    instances_info = aws_conn.instances()

    head = TEMPLATES['default'][0]
    foot = TEMPLATES['default'][1]

    monitoring = state = security_group = private_ip = name = None

    index = os.path.join(project_dir, 'index.html')

    logging.info('[*] Parsing AWS information and writing into index.html file..')
    file = open(index, 'a')
    file.write(head)

    for instance in instances_info:
        file.write('<tr>')
        info = instance['Instances'][0]

        for tag in sorted(info):
            if tag == 'Monitoring':
                monitoring = info[tag]['State']
                continue

            if tag == 'State':
                state = info[tag]['Name']
                continue

            if tag == 'SecurityGroups':
                sg = info[tag]
                if len(sg) != 0:
                    if 'GroupName' in sg[0]:
                        security_group = sg[0]['GroupName']
                        continue

            if tag == 'NetworkInterfaces':
                if len(info[tag]) != 0:
                    private_ip = info[tag][0]['PrivateIpAddress']
                    continue

            if tag == 'Tags':
                for _tags in info[tag]:
                    if _tags['Key'] == 'Name':
                        name = _tags['Value']
                        continue

            if tag in ['BlockDeviceMappings', 'IamInstanceProfile']:
                continue

        file.write('<td>{0}</td>'.format(name.lower()))
        file.write('<td>{0}</td>'.format(security_group.lower()))
        file.write('<td>{0}</td>'.format(monitoring))
        file.write('<td>{0}</td>'.format(private_ip))
        file.write('<td>{0}</td>'.format(state))
        file.write('</tr>')

    file.write(foot)

    print('[*] Done!')
    exit(0)
