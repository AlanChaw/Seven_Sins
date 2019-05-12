## Automation

### Introduction

In this assignment, we use Ansible to realize the function of automation. With one script, we can apply the instances from Nectar, then setup a CouchDB cluster among the virtual machines and make the webpage ready to run (but the databases are empty at this moment, to populate them, we need to log into the masternode server and run a bash script which is uploaded by Ansible).

### How to Work

We just need to execute `run.sh`, then input the password of openstack API and localhost, then the script will automatically complete the tasks mentioned above.

### Project Structure

```txt
.
├── Group58.pem
├── ansible.cfg
├── apply-instance.yml
├── background-configuration.yml
├── couchdb-cluster-setup.yml
├── docker-configuration.yml
├── environment-reset.yml
├── inventory.ini
├── openstack-api-password-Group58.txt
├── roles
│   ├── background-configuration
│   │   └── tasks
│   │       ├── data-populate.sh
│   │       └── main.yml
│   ├── couchdb-masternode
│   │   └── tasks
│   │       ├── main.yml
│   │       └── masternode.sh
│   ├── couchdb-subnode1
│   │   └── tasks
│   │       ├── main.yml
│   │       └── subnode1.sh
│   ├── couchdb-subnode2
│   │   └── tasks
│   │       ├── main.yml
│   │       └── subnode2.sh
│   ├── docker-configuration
│   │   └── tasks
│   │       └── main.yml
│   ├── openstack-common
│   │   └── tasks
│   │       └── main.yml
│   ├── openstack-images
│   │   └── tasks
│   │       └── main.yml
│   ├── openstack-instance
│   │   └── tasks
│   │       └── main.yml
│   ├── openstack-security-groups
│   │   └── tasks
│   │       └── main.yml
│   ├── reset
│   │   └── tasks
│   │       ├── main.yml
│   │       └── stop-containers.sh
│   ├── template-rendering
│   │   ├── tasks
│   │   │   └── main.yml
│   │   └── templates
│   │       ├── data-populate.sh.j2
│   │       ├── food_data.js.j2
│   │       ├── inventory.ini.j2
│   │       ├── job_data.js.j2
│   │       ├── masternode.sh.j2
│   │       ├── shopping_data.js.j2
│   │       ├── subnode1.sh.j2
│   │       └── subnode2.sh.j2
│   └── wait-for-port
│       └── tasks
│           └── main.yml
├── run.sh
├── unimelb-comp90024-group-58-openrc.sh
├── variables
│   └── variables.yml
└── web
    └── visualization
```

### Apply Instance

### Render Template

### Install Docker

### Setup CouchDB Cluster

### Setup Apache Server

### Conclusion

