# check out git code to server (assume that docker and couchdb containers are deployed)

export masternode=115.146.84.106
export user=admin
export password=123456

echo "=============checkout Background code from github==================="
cd ~
sudo apt-get install git
git init
git clone http://AlanChaw:binbin1124@github.com/AlanChaw/90024.git
cd 90024/
git checkout origin/Background
echo "=============Done==================="
echo "  "

# solve cross-origin problem

echo "=============allow Couchdb receive cross-origin access==================="
{
curl -X PUT http://${user}:${password}@${masternode}:5984/_node/couchdb@${masternode}/_config/httpd/enable_cors -d '"true"'
curl -X PUT http://${user}:${password}@${masternode}:5984/_node/couchdb@${masternode}/_config/cors/origins -d '"*"'
curl -X PUT http://${user}:${password}@${masternode}:5984/_node/couchdb@${masternode}/_config/cors/methods -d '"GET, PUT, POST, HEAD, DELETE"'
} &> /dev/null
echo "=============Done==================="
echo "  "

echo "=============Deploy geojson data==================="
curl -X PUT http://${user}:${password}@${masternode}:5984/geo_origin
{
  curl -X POST "http://${user}:${password}@${masternode}:5984/geo_origin " --header "Content-Type: application/json" --data @/home/ubuntu/90024/Background/MyCouchdb/geo_melb/origin_melb.json
}&> /dev/null
echo "=============Done==================="
echo "  "


echo "=============replicate database from analyse server==================="

curl -X PUT http://${user}:${password}@${masternode}:5984/food_twitters
curl -X PUT http://${user}:${password}@${masternode}:5984/shopping_twitters
curl -X PUT http://${user}:${password}@${masternode}:5984/job_twitters
{
  curl -X POST -H 'Content-Type: application/json' -d '{"source":"http://${user}:${password}@115.146.92.183:5984/food_twitters","target":"http://${user}:${password}@${masternode}:5984/food_twitters"}' http://${user}:${password}@${masternode}:5984/_replicate
  curl -X POST -H 'Content-Type: application/json' -d '{"source":"http://${user}:${password}@115.146.92.183:5984/shopping_twitters","target":"http://${user}:${password}@${masternode}:5984/shopping_twitters"}' http://${user}:${password}@${masternode}:5984/_replicate
  curl -X POST -H 'Content-Type: application/json' -d '{"source":"http://${user}:${password}@115.146.92.183:5984/job_twitters","target":"http://${user}:${password}@${masternode}:5984/job_twitters"}' http://${user}:${password}@${masternode}:5984/_replicate
} &> /dev/null

echo "=============replication OK==================="
echo "  "

# download nodejs code and install nodejs

echo "=============Deploy nodejs and Grunt environment==================="
{
  cd ~
  wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz
  tar xf node-v10.15.3-linux-x64.tar.xz


  cd node-v10.15.3-linux-x64/
  ./bin/node -v

  sudo ln -s ~/node-v10.15.3-linux-x64/bin/node /usr/bin
  sudo ln -s ~/node-v10.15.3-linux-x64/bin/npm /usr/bin
} &> /dev/null


# check nodejs and npm ready
echo "nodejs version"
node -v
echo "npm version"
npm -v

# compile and push views to couchdb
{
  cd ~
  npm install -g grunt-cli
  PATH=$PATH:$HOME/bin:/home/ubuntu/node-v10.15.3-linux-x64/bin

  cd /home/ubuntu/90024/Background

  npm install grunt --save-dev
  npm install grunt-cli --save-dev
  npm install grunt-couch --save-dev
} &> /dev/null
echo "=============Done==================="
echo "  "

echo "=============Compile and push map-reduce views==================="
grunt couch-compile
grunt couch-push


echo "======generating views==================="
{
curl http://${masternode}:5984/food_twitters/_design/designs/_view/agg_by_region?group=true
curl http://${masternode}:5984/shopping_twitters/_design/designs/_view/agg_by_region?group=true
curl http://${masternode}:5984/job_twitters/_design/designs/_view/agg_by_region?group=true
}&> /dev/null
echo "=============Done==================="
