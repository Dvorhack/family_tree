#! /bin/bash

echo "Stopping mysql"
docker stop mysql
docker rm mysql
docker stop phpmyadmin
docker rm phpmyadmin

echo "Stopping flask"
screen -XS flask quit

echo "Stopping VueJS"
screen -XS vuejs quit