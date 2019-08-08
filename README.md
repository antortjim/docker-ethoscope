
# Spin up a container
docker run --rm -P  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name ethoscope ethoscope

# Enter the container
docker exec -it ethoscope /bin/bash

# Start the services
systemctl start ntpd.service

tting up ssh server
systemctl start sshd.service

 host the bare git repo
systemctl start git-daemon.socket


systemctl daemon-reload

systemctl start ethoscope_node.service
systemctl start ethoscope_backup.service
systemctl start ethoscope_video_backup.service


systemctl daemon-reload
systemctl start ethoscope_update_node.service
