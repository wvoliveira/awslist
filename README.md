[![build status](http://gitlab.devel/wellingtonoliveira/awslist/badges/master/build.svg)](http://gitlab.devel/wellingtonoliveira/awslist/commits/master)
AWSLIST
-------

Lista as VMS no formato tabela (HTML) na AWS separando por nome, grupo de segurança, status de monitoramento, ip e estado da VM.

Exemplo:

```
cd awslist
pip2.7 -r requirements.txt
python2.7 awslist.py -c conf/config-example.ini > index.html
```
