#! /bin/bash

#docker run -dP --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name node  node && docker exec node /root/startup.sh || docker stop node
#i=1; docker run -dP --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name ETHOSCOPE_00$i ethoscope && docker exec ETHOSCOPE_00$i /root/startup.sh  || docker stop ETHOSCOPE_00$i


echo "Creating ethoscope-net network"
docker network create ethoscope-net

echo "Running mysql container with user and password root and name mysqld"
docker run --rm --name mysqld --net ethoscope-net -p 3306 -e MYSQL_ROOT_PASSWORD="root" -d mysql 

#MYSQL_PORT=$(docker port mysqld 3306 | cut -f 2 -d:)
#echo "mysql port is $MYSQL_PORT"
#echo "Removing root password"
#sleep 30 && mysqladmin -P $MYSQL_PORT --protocol=tcp -u root  -proot password ''
#echo "Creating ethoscope user with password ethoscope"
#mysql -P $MYSQL_PORT --protocol=tcp -u root  -e "CREATE USER 'ethoscope'@'%' IDENTIFIED BY 'ethoscope';"
#echo "Grating all privileges to ethoscope user"
#mysql -P $MYSQL_PORT --protocol=tcp -u root  -e "GRANT ALL PRIVILEGES ON *.* TO 'ethoscope'@'%' WITH GRANT OPTION;"

echo "Running node container"
docker run -dP --rm  --net ethoscope-net --name node  node

echo "Running ethoscope container"
docker run -dP --rm  --net ethoscope-net --name ETHOSCOPE_001 ethoscope

