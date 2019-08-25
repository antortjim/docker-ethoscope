# Ethoscope Docker image


An image that ports the ethoscope GUI to Docker for easy deployment and testing of new features

## How to run

```
# Spin up a container
docker run -P --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name ethoscope  ethoscope

# Check which host port is mapped to port 80
docker ps

# returns an output that looks like this
# aaba52d288ef        ethoscope           "/lib/systemd/systemd"   5 minutes ago       Up 5 minutes        0.0.0.0:32770->80/tcp   ethoscope
# it tells us that the container's port 80 has been mapped to host port 32770

# Enter the container
docker exec -it ethoscope /bin/bash

# IN THE CONTAINER
## Start the systemd services and the python server
systemctl enable sshd.service
systemctl start sshd.service
systemctl start git-daemon.socket
systemctl enable git-daemon.socket
systemctl daemon-reload
systemctl enable ethoscope_node.service
systemctl enable ethoscope_backup.service
systemctl enable ethoscope_video_backup.service
systemctl daemon-reload
systemctl enable ethoscope_update_node.service
cd /opt/ethoscope-git/node_src/scripts
python /opt/ethoscope-git/node_src/scripts/server.py --port 80


```

Open Chrome and navigate to the IP+Port address shown in the output of docker docker ps, in this case 0.0.0.0:32770
You should get an ethoscope table.




