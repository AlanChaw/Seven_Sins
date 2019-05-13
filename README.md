# COMP90024 - Team 58 - Seven Sins Project

- [Team Members](#Team-Members)
- [Introduction](#Introduction)
- [Cluster Configuration by Ansible Playbook](#Cluster-Configuration-by-Ansible-Playbook)
- [Data Harvest End](#Data-Harvest-End)
- [Data Analysis Pipeline](#Data-Analysis-Pipeline)
- [CouchDB Cluster Backend](#CouchDB-Cluster-Backend)
- [Web-based Visualization End](#Web-based-Visualization-End)
- [Potential Problems Solution](#Potential-Problems-Solution)

## Team Members
**Zisu Geng** - zisu.geng@student.unimelb.edu.au  
**Wenbin Cao** - wenbin.cao@student.unimelb.edu.au  
**Haopeng Yan** - haopeng.yan@student.unimelb.edu.au  
**Zhijun Chen** - zhijun.chen@student.unimelb.edu.au  
**Zemin Yu** - zemin.yu@student.unimelb.edu.au  


## Introduction 

The figure below displays the architecture of the system, we allocate one Nectar Cloud instance for data harvest and analysis (preprocess and sentiment analysis), while a three-node CouchDB cluster is deployed on the other three instances to provide RESTful APIs access for the visualization frontend. The details of the system is introduced in the final report. 

![System Architecture](./Pictures/Structure_final.png)  

Following is the instruction to deploy our whole system, which including:  

- Cluster Configuration
- Data Harvester End
- Data Analysis Pipeline
- CouchDB Cluster Backend
- Web-based Visualization End

## Cluster Configuration by Ansible Playbook

For the user who first use this scirpt, install the `ansible` and `Jinja2`  in advance

For Linux User

```bash
sudo apt-get install ansible
pip install Jinja2
```

For Mac User

```bash
brew install ansible
pip install Jinja2
```

then just execute the command

```bash
./run.sh
```

Input the password for openstack-api, which is offered in `openstack-api-password-Group58.txt` and localhost, then just wait.

After the application of instances, you can find 3 new virtual machines on Nectar.

![instance](./Pictures/Instances.png)

Then log into any node, and execute the command

```bash
curl -X GET http://admin:123456@localhost:5984/_membership
```

then the CouchDB cluster configuration can be checked.

![CouchDB-Cluster](./Pictures/couchdb-cluster.png)

## Data Harvest End

Both of the Data Harvest End and Data Analysis Pipeline has to be run on the "Preprocess" instance which is created before. Meanwhile, a stand-alone single node CouchDB is required to be deployed on this instance by docker:

``` bash
docker run -d -p 5984:5984 --name=subcouchdb1 couchdb:2.3.0
```

We support two script to Harvest the twitter data, one is gathering data directly by the Twitter Developer APIs, another one is gathering data from the existing CouchDB supplied in the assignment instructions:

``` bash
cd ${Project_path}/Data_Harvest/
python3 searcher.py
python3 streamer.py
```

## Data Analysis Pipeline

The Data Analysis Pipeline requires to run on the "Preprocess" Nectar Cloud instance. A local stand-alone CouchDB has to be configured on this instance. 

The NLTK (Natural Language Toolkit) and WordNet package for NLTK is required to be install prior.

``` bash
$ pip3 install nltk  
$ python3  
```

``` python
import nltk
nltk.download('wordnet')
```

To run the Analysis Pipeline, just go to the Analysis folder and run script:

``` bash  
cd ${Project_path}/Analyze/  
chmod 777 process_all.sh  
./process_all.sh  
```

The analysis script will automatically classify the data for different scenarios and do the sentiment analysis task. The processed twitters will be output to the local CouchDB:

<img src="./Pictures/CouchDB_generated.png" height="50%" width="50%">

This part usually takes about 20 minutes to run.

## CouchDB Cluster Backend

To populate the data to the CouchDB Cluster, compile and push MapReduce views, we build a script which can run all tasks automatically. This script is required run on the "instance 0" Nectar instance (the instance that configured the CouchDB master node). The script will be upload to the "instance 0" by Ansible when the instance is prepared.

To run the data populate script, just run following commands:

``` bash  
cd ${Project_path}/Backend/  
chmod 777 data-populate.sh  
./data-populate.sh  
```

The script will checkout the newest code from this respository, replicate twitter data from the stand-alone instance before, compile and push MapReduce views by Grunt. The Node.js and Grunt dependencies will also be installed by the script itself.

After the execution of this script, we can see that the MapReduce views has pushed to the databases successfully:

<img src="./Pictures/Backend_result.png" height="50%" width="50%"> 

If we send a get request to the CouchDB cluster by:

```
http://${cluster_IP}:5984/food_twitters/_design/designs/_view/agg_by_region?group=true
```

A list of JSON response like below will be returned:

```javascript
{  
      "key": {  
        "name": "Abbotsford"  
      },  
      "value": {  
        "positive": 98,  
        "negative": 21,  
        "neutral": 65,  
        "total": 184 
      }  
    }  
}  
```


## Web-based Visualization End

The web visualization end will be automatically deployed by the Ansible Playbook. It just runs in the Docker Container on the same Nectar Cloud instance of the CouchDB master node. So there is no need to configure the web end manually. 

We deployed a backup web visulisation end which can be access by the link below (Only allow access in Unimelb or with Unimelb VPN): 

[Project Visualization Website](http://115.146.92.183/homepage.html)

![Website](./Pictures/Website.png)

## Potential Problems Solution

For the user who has created the instances and Docker environment, but get bug in the continuing steps, please open the `run.sh`, then comment the line 4, 7 and uncomment line 10, which makes the bash script's content is

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

