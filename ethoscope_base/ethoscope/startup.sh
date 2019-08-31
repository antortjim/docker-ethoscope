#! /bin/bash

## Enable networktime protocol
#systemctl daemon-reload
#systemctl enable ethoscope_device.service
#systemctl start ethoscope_device.service
#systemctl enable ethoscope_update.service
#systemctl start ethoscope_update.service
#systemctl start mysqld.service
#systemctl enable mysqld.service

USER_NAME=ethoscope
PASSWORD=ethoscope
MYSQL_PORT=3306
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "CREATE USER \"$USER_NAME\"@'localhost' IDENTIFIED BY \"$PASSWORD\""
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "CREATE USER \"$USER_NAME\"@'%' IDENTIFIED BY \"$PASSWORD\""
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "GRANT ALL PRIVILEGES ON *.* TO \"$USER_NAME\"@'localhost' WITH GRANT OPTION";
mysql -h mysqld -proot -P $MYSQL_PORT -u root -e "GRANT ALL PRIVILEGES ON *.* TO \"$USER_NAME\"@'%' WITH GRANT OPTION";

touch /etc/mysql/my.cnf
#echo "innodb_buffer_pool_size = 128M" >> /etc/mysql/my.cnf
#echo "innodb_log_file_size = 32M" >> /etc/mysql/my.cnf
#echo "innodb_log_buffer_size = 50M" >> /etc/mysql/my.cnf
#echo "innodb_flush_log_at_trx_commit = 1" >> /etc/mysql/my.cnf
#echo "innodb_lock_wait_timeout = 50" >> /etc/mysql/my.cnf
#echo "innodb_file_per_table=1" >> /etc/mysql/my.cnf


##systemctl disable systemd-networkd
## Enable networktime protocol
#systemctl start ntpd.service
#systemctl enable ntpd.service
## Setting up ssh server
#systemctl enable sshd.service
#systemctl start sshd.service
#
#systemctl daemon-reload
#systemctl start ethoscope_device.service
#systemctl enable ethoscope_device.service
#systemctl start ethoscope_update.service
#systemctl enable ethoscope_update.service
#sudo systemctl enable watchdog
#sudo systemctl start watchdog

## Identity
cd /opt/ethoscope-git/src/scripts/
/usr/bin/python3 /opt/ethoscope-git/src/scripts/device_server.py -D
