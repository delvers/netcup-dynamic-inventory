### Ansible dynamic inventory script for netcup
This script provides a [dynamic inventory](http://docs.ansible.com/ansible/intro_dynamic_inventory.html) for ansible, based on SOAP interface provided by netcup.

#### Usage
    usage: scp.py [-h] [-H] [-l] [--host HOST] [-c {start,stop}]

    Ansible dynamic inventory script for netcup scp (and also some kind of cli)

    optional arguments:
      -h, --help       show this help message and exit
      -H, --human      makes the output more readable for human
      -l, --list       list servers with id and full hostname
      --host HOST      show additional attributes of the given server
      -c {start,stop}  starts or stops server, requires --host

#### Install
This script is developed with Python 2.7.12 and based on [zeep](http://docs.python-zeep.org/en/master/).
Zeep is fastly installed:

    pip install zeep

It requires also the credentials for the [webservice interface]("https%3A%2F%2Fwww.netcup-wiki.de%2Fwiki%2FServer_Control_Panel_%28SCP%29%23Webservice").
So copy the file `passwd.cfg.example` to `passwd.cfg` and fill it with your credentials.

    cp ./passwd.cfg.example ./passwd.cfg

After editing the credentials it should be possible to ping your netcup hosts with ansible:

    ansible -i ./netcupdi.py all -m ping
