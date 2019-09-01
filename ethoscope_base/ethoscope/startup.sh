#! /bin/bash

USER_NAME=ethoscope
PASSWORD=ethoscope
NAME="ethoscope_db"
MYSQL_PORT=3306
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "RESET MASTER";
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "DROP DATABASE IF EXISTS $NAME";


mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "CREATE USER \"$USER_NAME\"@'localhost' IDENTIFIED BY \"$PASSWORD\""
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "CREATE USER \"$USER_NAME\"@'%' IDENTIFIED BY \"$PASSWORD\""
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "GRANT ALL PRIVILEGES ON *.* TO \"$USER_NAME\"@'localhost' WITH GRANT OPTION";
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "GRANT ALL PRIVILEGES ON *.* TO \"$USER_NAME\"@'%' WITH GRANT OPTION";

## Identity
cd /opt/ethoscope-git/src/scripts/
/usr/bin/python3 /opt/ethoscope-git/src/scripts/device_server.py -D
