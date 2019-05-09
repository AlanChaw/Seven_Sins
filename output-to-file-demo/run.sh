#!/bin/bash

. open.sh; ansible-playbook --ask-become-pass main.yml
