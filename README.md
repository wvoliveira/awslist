[![build status](https://travis-ci.org/wvoliveira/awslist.svg?branch=master)](https://travis-ci.org/wvoliveira/awslist)

AWSLIST
-------

List AWS EC2 in HTML format. Separated by name, security group, monitoring status, IP e VM state.


Tested
------

Python3 > 


How to
-----

Download e configure
```bash
git clone git@github.com:wvoliveira/awslist.git
cd awslist
pip3 install -U .
```

```bash
awslist -h
usage: awslist [-h] [--region] [--credentials] directory

List EC2 VMs HTML format.
https://github.com/wvoliveira/awslist

positional arguments:
  directory

optional arguments:
  -h, --help       show this help message and exit
  --region       region
  --credentials  credentials
```

Example AWS credentials file (default: ~/.aws/credentials):
```
[default]
aws_access_key_id = KEYHEREKEYHEREKEYHEREKEYHERE
aws_secret_access_key = KEYHEREKEYHEREKEYHEREKEYHERE
```

Just run:
```
awslist teste
```

Output:
```bash
[*] Creating project structure...
[+] Project directory: /data/teste
[*] Copying files into the project directory..
[*] Collecting AWS credentials..
[*] Trying to connect to AWS..
[*] Collecting information from AWS..
Starting new HTTPS connection (1): ec2.sa-east-1.amazonaws.com
[*] Parsing AWS information and writing into index.html file..
[*] Done!
```

Jump to contents directory, open web server and look in your browser:
```bash
cd teste
python3 -m http.server
http://127.0.0.1:8000/
```

Looks nice, no?
