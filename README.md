# Frontend
vuejs
single web page

build command: npm run build

# Backend
flask

api 
 -> add_user
 -> del_user
 -> modify_user
 -> get_user
 -> get_all_user

# BDD

table user
 -> nom
 -> prénom
 -> date naissance

table liens
 -> personne1
 -> lien e parenté
 -> personne2

 liens possibles: enfant, conjoint

# Start the project
## Requirements
docker
scree
python:
    flask
    flask-cors
    python-dotenv
    flask-sqlalchemy
    sqlalchemy
    networkx
    numpy
    matplotlib
    mysqlclient
    wheel

npm:
    sudo @vue/cli
    axios
    eslint
    vue-router
    bootstrap
    vue-tree-chart --save
    npm install vue-family-tree --save
    @balkangraph/familytree.js

if fucking ubuntu user: curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -

## Config
You must create a .env file in the server folder and fill in the following variables:
MASTER_PASSWD=marchand
MYSQL_USER=root
MYSQL_PASSWD=root
MYSQL_DB=Genealogical
MYSQL_SERVER=127.0.0.1:3306

You can open the .env.example to see the required format

## Run
if all the requirements are satisfied, you just need to run ./run.sh
The database will start in docker and the front/back in two different screen

in order to view the front/back output you can run `screen -r flask` or `screen -r vuejs`

## Stop
To stop everything, just run the `stop.sh` script 

# TODO
scritp install
