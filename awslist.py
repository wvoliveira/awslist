#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import ConfigParser
import argparse
import datetime
import logging
import awslist.aws as aws

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="""List AWS VMs\nhttp://gitlab.devel/infra/awslist""")

logging.basicConfig(stream=sys.stdout, level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

parser.add_argument('-c', '--config', metavar='\b', help='config file', required=True)
args = parser.parse_args()


def config_parser(section):
    config = ConfigParser.ConfigParser()
    config.read(args.config)
    if config.has_section(section):
        items_dict = dict(config.items(section))
        return items_dict
    else:
        logging.error("Variavel '{0}' inexistente no arquivo de configuracao".format(section))
        sys.exit(1)


def difference_date(date_):
    date = datetime.datetime.strptime(str(date_), '%Y-%m-%d %H:%M:%S')
    difference = abs(datetime.datetime.now() - date)
    return difference.days


def main():
    try:
        aws_args = config_parser('aws')
    except Exception as error:
        logging.error('Error to parse AWS sections: {0}'.format(error))
        sys.exit(2)

    try:
        region = aws_args['region']
        key_id = aws_args['key_id']
        access_key = aws_args['access_key']
        owner_id = aws_args['owner_id']
    except Exception as error:
        logging.error('Error to collect credentials: {0}'.format(error))
        sys.exit(2)

    try:
        aws_conn = aws.AWS(region, key_id, access_key, owner_id)
    except Exception as error:
        logging.error('Error to connect in Amazon AWS: {0}'.format(error))
        sys.exit(2)

    instances_info = aws_conn.instances()

    print("""
<!DOCTYPE html>
<html lang="en">
<head>
<title>AWS VMs</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/bootstrap.min.css">
<script src="js/jquery.min.js"></script>
<script src="js/bootstrap.min.js"></script>
</head>
<body>

<div class="container">
<h2>AWS VMs</h2>
<p>Algum texto maneiro que vou inserir aqui, mas eh isso ai galera.</p>
<table class="table">
<thead>
<tr>
<th>Name</th>
<th>Security Group</th>
<th>Monitoring</th>
<th>IP</th>
<th>State</th>
</tr>
</thead>
<tbody>
        """)

    monitoring = None
    state = None
    security_group = None
    private_ip = None
    name = None

    for instance in instances_info:
        print('<tr>')
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
                    if sg[0].has_key('GroupName'):
                        security_group = sg[0]['GroupName']
                        continue

            if tag == 'NetworkInterfaces':
                if len(info[tag]) != 0:
                    private_ip = info[tag][0]['PrivateIpAddress']
                    # print('{0}: {1}'.format(tag, info[tag][0]['PrivateIpAddress'], info[tag][0]['Status']))
                    continue

            if tag == 'Tags':
                for _tags in info[tag]:
                    if _tags['Key'] == 'Name':
                        name = _tags['Value']
                        continue

            if tag in ['BlockDeviceMappings', 'IamInstanceProfile']:
                continue


        print('<td>{0}</td>'.format(name.lower()))
        print('<td>{0}</td>'.format(security_group.lower()))
        print('<td>{0}</td>'.format(monitoring))
        print('<td>{0}</td>'.format(private_ip))
        print('<td>{0}</td>'.format(state))
        print('</tr>')

    print("""
</tbody>
</tbody>
</table>
</div>

</body>
</html>
    """)


if __name__ == '__main__':
    main()
