#!/bin/bash

usermod -a -G docker ubuntu
newgrp docker
