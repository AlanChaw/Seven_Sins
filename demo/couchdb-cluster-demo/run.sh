#!/bin/bash

. ./openrc.sh; ansible-playbook -i inventory.ini -u ubuntu --key-file=./keypair0 main.yml
