## This Dockerfile provides a way to virtualize an Arch Linux OS with systemd support in Docker
FROM ethoscope_base 
LABEL maintainer "Antonio Ortega <antonio.ortega@kuleuven.vib.be>"

#Create a local working copy from the bare repo on node
#RUN git clone /srv/git/ethoscope.git /opt/ethoscope-git
# ethoscope dependencies not installed by pip
#RUN pacman -S --noconfirm hdf5
#RUN pacman -S --noconfirm opencv
#RUN pacman -S --noconfirm gtk3
#RUN pip install h5py==2.6.0
RUN cd /opt/ethoscope-git/node_src && pip install -e .

# Expose port 80 for the ethoscope_node service and 8888 for the updater
EXPOSE 80
EXPOSE 8888

# Copy the startup script executed with docker exec right after docker run
# This script cannot be passed as ENTRYPOINT because systemd must be for the services to work
COPY startup.sh /root/

ENV init /lib/systemd/systemd
VOLUME [ "/sys/fs/cgroup" ]
ENTRYPOINT ["/lib/systemd/systemd"]
