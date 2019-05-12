## Automation

### Introduction

In this assignment, we use Ansible to realize the function of automation. With one script, we can apply the instances from Nectar, then setup a CouchDB cluster among the virtual machines and make the webpage ready to run (but the databases are empty at this moment, to populate them, we need to log into the masternode server and run a bash script which is uploaded by Ansible).

### How to Work

We just need to execute **run.sh**, then input the password of openstack API and localhost, then the script will automatically complete the tasks mentioned above.

### Project Structure

![structure](./images/structure.png)

### Sepcific Process

1. Apply Instance
2. Render Templates
3. Install Docker
4. Setup CouchDB Cluster
5. Setup Apache Server

### Apply Instance

In this step, we reference the demo in Lecture 5, which shows how to use Ansible to apply one instance. We apply 3 instances in this assignment, set one instance as the masternode of CouchDB cluster and the other two as the subnodes. An exclusive instance(IP address is 115.146.92.183) has been applied in advance for harvast program, data collecting and visualization display.

#### Instance Variables

- Image: NeCTAR Ubuntu 16.04 LTS (Xenial) amd64 
- Flavor: m1.small
- Availability Zone: melbourne-qh2
- Security: We open the port 22 for ssh connection, port 80 for http access, and port 5984 for CouchDB's operations.

We set a task for the instances to wait 240 seconds since when they have been created. The reason why we do this is to ensure the enough time before the port 22 of each instance has been opened. If the waiting time is too short, the ssh connection to the virtual machines may fail.

![waiting](./images/waiting.png)

And we solve the problem that if we use Ansible to connect serveral instances by ssh for the first time, the prompts from serveral virtual machines to the user to input "yes/no" will conflict to each other, then fail the connection. We create an **ansible.cfg** file in the playbook directory, which can skip the prompt when connect instances via ssh.

![ansible-cfg](./images/ansible-cfg.png)

### Render Template

A very important step for the automation is that we need use some bash scripts to complete the operations. So we need put the IP address into these scripts. In addition, Ansible also need the IP address to tell which servers should complete the current tasks.

![ip-in-script](./images/ip-in-script.png)

Since the floating IP address is allocated by the application of instances, we use some variables to record them and make some Jinja2 templates, after the applications of instance, the templates will be rendered as the real scripts, JavaScript codes and configuration files to relevant locations.

![template-rendering](./images/template-rendering.png)

### Install Docker

We use Docker as a supporting tool in this assignment. The most useful characteristics of Docker is that we can reset the all the dependent environment of the image by killing the container, which is very convenient for developing.

In this step, we reference the demo in Lecture 5, which shows how to launch a Wordpress service by Docker via Ansible. And for the later step, we add three tasks for every instances in this role: add docker users, pull the image of CouchDB, pull the image of Apache.

### Setup CouchDB Cluster

### Setup Apache Server

### Conclusion

