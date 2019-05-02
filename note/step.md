### The Step of Auto Deployment

1. 一键化？
2. apply 4 instance
3. start the dockers (在每一个节点上分别启动还是在主节点上启动所有节点的dockers？)
4. setup the cluster

---

playbook folder

- variables - [defines all the variables using in the playbook eg. `the port to open` / `the software to install`]
  - vars.yml
- inventory - [defines the hosts the playbook access to]
  - inventory.ini
- roles - [modules, breaks a complex playbook into small pieces]
  - defaults
  - tasks - [actual things ansible to do]
    - task1.yml
    - task2.yml
  - templates / files [files will be uploaded / templates will be replaced by the values in variables then uploaded]
- playbook.yml [defines the configuration / deployment in ansible]

---

