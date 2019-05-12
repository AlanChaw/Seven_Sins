#!/bin/bash

# apply the instances, render the templates
# . ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook --ask-become-pass apply-instance.yml

# install docker on the remote servers
# . ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v docker-configuration.yml

# reset the enviroment of the remote servers
. ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v environment-reset.yml

# setup couchdb cluster on database servers
. ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v couchdb-cluster-setup.yml

# setup the web server and load the data
. ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v background-configuration.yml
