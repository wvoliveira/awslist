[![build status](https://travis-ci.org/wvoliveira/awslist.svg?branch=master)](https://travis-ci.org/wvoliveira/awslist)

AWSLIST
-------

Lista as VMS no formato tabela (HTML) na AWS separando por nome, grupo de segurança, status de monitoramento, ip e estado da VM.

Exemplo:

```
cd awslist
pip2.7 -r requirements.txt
python2.7 awslist.py -c conf/config-example.ini > index.html
```
