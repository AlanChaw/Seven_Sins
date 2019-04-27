
sudo apt-get install git
git init
git clone http://AlanChaw:binbin1124@github.com/AlanChaw/90024.git
cd 90024/
git checkout origin/Background


curl -X PUT http://localhost:5984/twitter
curl -X POST "http://localhost:5984/twitter/_bulk_docs " --header "Content-Type: application/json" --data @/home/ubuntu/90024/Background/MyCouchdb/twitter/melb.json


cd 90024/Background/

npm install -g grunt-cli
npm install grunt --save-dev
npm install grunt-couch --save-dev
npm install grunt-cli --save-dev


cd ~
wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz
tar xf node-v10.15.3-linux-x64.tar.xz


cd node-v10.15.3-linux-x64/
./bin/node -v


sudo ln -s ~/node-v10.15.3-linux-x64/bin/node /usr/bin
sudo ln -s ~/node-v10.15.3-linux-x64/bin/npm /usr/bin


cd ~
npm install -g grunt-cli
PATH=$PATH:$HOME/bin:/home/ubuntu/node-v10.15.3-linux-x64/bin


npm install grunt --save-dev
npm install grunt-cli --save-dev
npm install grunt-couch --save-dev

grunt couch-compile
grunt couch-push
