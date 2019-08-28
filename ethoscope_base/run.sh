#! /bin/bash

docker run -dP --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name node  node && docker exec node /root/startup.sh || docker stop node
i=1; docker run -dP --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name ETHOSCOPE_00$i ethoscope && docker exec ETHOSCOPE_00$i /root/startup.sh  || docker stop ETHOSCOPE_00$i

