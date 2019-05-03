#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass nectar.yml
