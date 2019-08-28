# Ethoscope Docker image


An image that ports the ethoscope GUI to Docker for easy deployment and testing of new features

## How to run

```
# Spin up a container for the node and run the appropriate services
# If the exec command fails, the container is stopped and removed automatically (thanks to --rm and docker stop node)
docker run -dP --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name node  node && docker exec node /root/startup.sh || docker stop node

# Check which host port is mapped to port 80
docker ps

# returns an output that looks like this
# aaba52d288ef        ethoscope           "/lib/systemd/systemd"   5 minutes ago       Up 5 minutes        0.0.0.0:32770->80/tcp   ethoscope
# it tells us that the container's port 80 has been mapped to host port 32770
```
Open Chrome and navigate to the IP+Port address shown in the output of docker docker ps, in this case [0.0.0.0:32770](0.0.0.0:32770)
You should get an emtpy ethoscope table.

![empty table](images/empty_table.png) 


```
i=1; docker run -dP --rm  --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name ETHOSCOPE_00$i ethoscope && docker exec ETHOSCOPE_00$i /root/startup.sh  || docker stop ETHOSCOPE_00$i
```

