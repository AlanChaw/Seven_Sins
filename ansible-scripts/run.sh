#!/bin/bash

# . ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook --ask-become-pass main.yml
. ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v --ask-become-pass main.yml
