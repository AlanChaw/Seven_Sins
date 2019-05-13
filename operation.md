## Instruction Book

- For the user who first use this scirpt, just execute the command

```bash
./run.sh
```

input the password for openstack-api, which is offered in `openstack-api-password-Group58.txt` and localhost, then just wait.

- For the user who has created the instances and Docker environment, but get bug in the continuing steps, please open the `run.sh`, then comment the line 4, 7 and uncomment line 10, which makes the bash script's content is

```bash
#!/bin/bash

# apply the instances, render the templates
# . ./unimelb-comp90024-group-58-openrc.sh; ansible-playbook --ask-become-pass apply-instance.yml

# install docker on the remote servers
# ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 docker-configuration.yml

# reset the enviroment of the remote servers
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 -v environment-reset.yml

# setup couchdb cluster on database servers
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 couchdb-cluster-setup.yml

# setup the web server and load the data
ansible-playbook -i inventory.ini -u ubuntu --key-file=./Group58 background-configuration.yml
```

then execute the command

```bash
./run.sh
```

---

