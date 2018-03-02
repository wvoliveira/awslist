"""
TODO:
Exceptions file
"""

import argparse
import logging
import sys
import os
import shutil
import tempfile
from colorama import Fore, Style
from .commands import config_parser, aws, TEMPLATES


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""List EC2 VMs HTML format.\nhttps://github.com/wvoliveira/awslist""")
    parser.add_argument('--region', default='sa-east-1', metavar='\b', help='region', required=False)
    parser.add_argument('--credentials', default='~/.aws/credentials', metavar='\b', help='credentials', required=False)
    parser.add_argument('--force', default=False, action='store_true', help='Force update folder')
    parser.add_argument('directory')
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
    logging.info('[*] Creating project structure...')

    if not args.force:
        if os.path.exists(args.directory):
            print('{0}[!]{1} This folder already exists! Exiting..')
            sys.exit(1)

    temp_dir = os.path.join(tempfile.mkdtemp(), args.directory)
    project_dir = os.path.join(os.path.abspath('.'), args.directory)
    package_dir = sys.modules['awslist'].__path__[0]

    logging.info('[+] Temporary: {0}{1}{2}'.format(Style.BRIGHT, temp_dir, Style.NORMAL))
    logging.info('[+] Project: {0}{1}{2}'.format(Style.BRIGHT, project_dir, Style.NORMAL))

    src_static_files = os.path.join(package_dir, 'data')
    dst_static_files = os.path.join(temp_dir, 'static')
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

    index = os.path.join(temp_dir, 'index.html')

    logging.info('[*] Parsing AWS information and writing into index.html file..')
    file = open(index, 'a')
    file.write(head)

    security_groups = private_ip = name = None

    for instance in instances_info:
        file.write('<tr>')
        vm = instance['Instances'][0]

        try:
            name = ''.join(x['Value'] for x in vm['Tags'] if x['Key'] == 'Name')
        except:
            pass

        monitoring = vm['Monitoring']['State']
        state = vm['State']['Name']

        try:
            security_groups = ', '.join(name['GroupName'] for name in vm['SecurityGroups'])
        except:
            pass

        try:
            private_ip = vm['NetworkInterfaces'][0]['PrivateIpAddress']
        except:
            pass

        zone = vm['Placement']['AvailabilityZone']
        _type = vm['InstanceType']
        _key = vm['KeyName']
        instance_id = vm['InstanceId']
        image_id = vm['ImageId']
        private_dns = vm['PrivateDnsName']

        file.write('<td>{0}</td>'.format(name.lower()))
        file.write('<td>{0}</td>'.format(private_ip))
        file.write('<td>{0}</td>'.format(security_groups.lower()))
        file.write('<td>{0}</td>'.format(monitoring))
        file.write('<td>{0}</td>'.format(state))
        file.write('<td>{0}</td>'.format(zone))
        file.write('<td>{0}</td>'.format(_type))
        file.write('<td>{0}</td>'.format(_key))
        file.write('<td>{0}</td>'.format(instance_id))
        file.write('<td>{0}</td>'.format(image_id))
        file.write('<td>{0}</td>'.format(private_dns))
        file.write('</tr>')

    file.write(foot)

    if args.force:
        if os.path.exists(args.directory):
            shutil.rmtree(args.directory)

    logging.info('[*] Moving from {0}{2}{1} to {3}.. '.format(Style.BRIGHT, Style.NORMAL, temp_dir, project_dir))
    shutil.move(temp_dir, project_dir)

    print('[*] Done!')
    exit(0)
