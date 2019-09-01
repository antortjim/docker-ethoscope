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

# Copy the startup script executed with docker exec right after docker run
# This script cannot be passed as ENTRYPOINT because systemd must be for the services to work
COPY *.sh /root/
RUN chmod +x /root/*.sh

EXPOSE 80
ENTRYPOINT ["/root/start_node.sh"]
