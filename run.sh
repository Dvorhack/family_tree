#! /bin/bash


SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
cd $SCRIPT_DIR
echo "Script dir: $PWD"

# Start docker container for mysql & phpmyadmin
echo "Starting mysql"
docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:latest
echo "Starting phpymadmin"
docker run --name phpmyadmin -d --link mysql:db -p 8081:80 phpmyadmin/phpmyadmin:latest

# start backend
echo "Starting flask"
backend_name=flask
screen -dmS $backend_name
screen -S $backend_name -X stuff "cd server && source env/bin/activate && python app.py\n"

# start front
echo "Starting VueJS"
backend_name=vuejs
screen -dmS $backend_name
screen -S $backend_name -X stuff "cd client && npm run serve\n"