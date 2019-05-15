#!/bin/bash

# apply the instances, render the templates
. ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook --ask-become-pass apply-instance.yml

# install docker on the remote servers
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 docker-configuration.yml

# reset the enviroment of the remote servers
# ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v environment-reset.yml

# setup couchdb cluster on database servers
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 couchdb-cluster-setup.yml

# setup the web server and load the data
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 background-configuration.yml
