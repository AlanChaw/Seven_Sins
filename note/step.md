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

目前的投机Solution

在最终的`run.sh`中，首先第一阶段的ansible文件，生成4个instance并将其IP地址输出到一个临时文件中，之后执行一个Python脚本读取IP地址并生成inventory文件，之后再运行安装环境的yaml文件

ansible的lineinfile可以做输出，可以考虑是否能合并到一步完成

---

