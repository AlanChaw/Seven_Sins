

# check out git code to server (assume that docker and couchdb containers are deployed)
cd ~
sudo apt-get install git
git init
git clone http://AlanChaw:binbin1124@github.com/AlanChaw/90024.git
cd 90024/
git checkout origin/Background

# solve cross-origin problem
curl -X PUT http://admin:123456@115.146.92.183:5984/_node/couchdb@127.0.0.1/_config/httpd/enable_cors -d '"true"'
curl -X PUT http://admin:123456@115.146.92.183:5984/_node/couchdb@127.0.0.1/_config/cors/origins -d '"*"'
curl -X PUT http://admin:123456@115.146.92.183:5984/_node/couchdb@127.0.0.1/_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'

# create couchdb and push geojson and AURIN data to couchdb
# curl -X PUT http://admin:123456@localhost:5984/twitter
# curl -X POST "http://admin:123456@localhost:5984/twitter/_bulk_docs " --header "Content-Type: application/json" --data @/home/ubuntu/90024/Background/MyCouchdb/twitter/melb.json
curl -X PUT http://admin:123456@localhost:5984/geo_origin
curl -X POST "http://admin:123456@localhost:5984/geo_origin " --header "Content-Type: application/json" --data @/home/ubuntu/90024/Background/MyCouchdb/twitter/origin_melb.json
# curl -X POST "http://admin:123456@localhost:5984/geo_origin " --header "Content-Type: application/json" --data @/home/ubuntu/90024/Background/MyCouchdb/twitter/victoria.json
curl -X PUT http://admin:123456@localhost:5984/aurin
curl -X POST "http://admin:123456@localhost:5984/aurin/_bulk_docs " --header "Content-Type: application/json" --data @/home/ubuntu/90024/Background/MyCouchdb/aurin/Restaurant.json



# download nodejs code and install nodejs
cd ~
wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz
tar xf node-v10.15.3-linux-x64.tar.xz


cd node-v10.15.3-linux-x64/
./bin/node -v

sudo ln -s ~/node-v10.15.3-linux-x64/bin/node /usr/bin
sudo ln -s ~/node-v10.15.3-linux-x64/bin/npm /usr/bin


# check nodejs and npm ready
node -v
npm -v


# compile and push views to couchdb

cd ~
npm install -g grunt-cli
PATH=$PATH:$HOME/bin:/home/ubuntu/node-v10.15.3-linux-x64/bin

cd /home/ubuntu/90024/Background

npm install grunt --save-dev
npm install grunt-cli --save-dev
npm install grunt-couch --save-dev


grunt couch-compile
grunt couch-push
