#!/bin/bash

. ./openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=~/.ssh/keypair0 main.yml
