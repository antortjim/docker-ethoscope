## This Dockerfile provides a way to virtualize an Arch Linux OS with systemd support in Docker
FROM systemd_arch
LABEL maintainer "Antonio Ortega <antonio.ortega@kuleuven.vib.be>"


## Installing extra packages
## https://qgeissmann.gitbooks.io/ethoscope-manual/building-and-installation/node.html#installing-extra-packages

# update all packages
RUN pacman -Syu --noconfirm

# tools for developers
RUN pacman -S base-devel git gcc-fortran rsync wget fping --noconfirm --needed

# utilities
RUN pacman -S ntp bash-completion openssh --noconfirm --needed

#so we can set up a dns
RUN pacman -S dnsmasq --noconfirm --needed

# pre-installing dependencies will save compiling time on python packages
RUN pacman -S python2-pip python2-numpy python2-bottle python2-pyserial mysql-python python2-netifaces python2-cherrypy python2-futures --noconfirm --needed

# mariadb
RUN pacman -S mariadb --noconfirm --needed

# setup Wifi dongle
RUN pacman -S wpa_supplicant --noconfirm --needed
RUN pacman -S libev --noconfirm --needed

# install python3
RUN pacman -Sy --noconfirm python python-pip
RUN pip install bottle

## Creating a git bare repo
## https://qgeissmann.gitbooks.io/ethoscope-manual/building-and-installation/node.html#creating-a-git-bare-repo

# a few variables
RUN UPSTREAM_GIT_REPO=https://github.com/gilestrolab/ethoscope.git
RUN LOCAL_BARE_PATH=/srv/git/ethoscope.git

# clone the git repo in the /srv/git dir
RUN mkdir -p /srv/git
#RUN git clone --bare https://github.com/gilestrolab/ethoscope.git /srv/git/ethoscope.git


## The node software
## https://qgeissmann.gitbooks.io/ethoscope-manual/building-and-installation/node.html#the-node-software
# variables
RUN TARGET_UPDATER_DIR=/opt/ethoscope_updater
RUN TARGET_GIT_INSTALL=/opt/ethoscope-git

#Create a local working copy from the bare repo on node
RUN echo 'Installing ethoscope package'
#RUN git clone /srv/git/ethoscope.git /opt/ethoscope-git


## IMPORTANT this is if you want to work on the "dev" branch otherwise, you are using "master"
RUN cd /opt/ethoscope-git && git branch && git checkout python3.7
#
## we install with pip
RUN cd /opt/ethoscope-git/node_src && pip install -e .


# ethoscope dependencies not installed by pip
RUN pacman -S --noconfirm hdf5 opencv
RUN pacman -S --noconfirm gtk3
RUN pip install h5py==2.6.0
RUN cd /opt/ethoscope-git/src && pip install -e .

### we create a symbolic link of the updated in the proper location
RUN ln -s /opt/ethoscope-git/scripts/ethoscope_updater /opt/ethoscope_updater

RUN cd /opt/ethoscope-git/scripts && cp ./ethoscope_node.service /etc/systemd/system/ethoscope_node.service && cp ./ethoscope_backup.service /etc/systemd/system/ethoscope_backup.service && cp ./ethoscope_video_backup.service /etc/systemd/system/ethoscope_video_backup.service

RUN cd /opt/ethoscope_updater && cp ethoscope_update_node.service /etc/systemd/system/ethoscope_update_node.service

RUN cd /etc/systemd/system && sed -i 's/ethoscope-node/ethoscope-git/' ethoscope_*.service 

RUN pacman -Sy --noconfirm vim

RUN printf "#! /bin/bash\n\nsystemctl enable sshd.service\nsystemctl start sshd.service\nsystemctl start git-daemon.socket\nsystemctl enable git-daemon.socket\nsystemctl daemon-reload\nsystemctl enable ethoscope_node.service\nsystemctl enable ethoscope_backup.service\nsystemctl enable ethoscope_video_backup.service\nsystemctl daemon-reload\nsystemctl enable ethoscope_update_node.service\n#python /opt/ethoscope-git/node_src/scripts/server.py --port 80\n" > /root/services.sh

RUN chmod +x /root/services.sh

EXPOSE 80
EXPOSE 8888
EXPOSE 9000


ENV init /lib/systemd/systemd
VOLUME [ "/sys/fs/cgroup" ]
ENTRYPOINT ["/lib/systemd/systemd"]


### Enable networktime protocol
#
#RUN systemctl start ntpd.service
#RUN systemctl enable ntpd.service
#
## Setting up ssh server
#RUN systemctl enable sshd.service
#RUN systemctl start sshd.service
#
## to host the bare git repo
#RUN systemctl start git-daemon.socket
#RUN systemctl enable git-daemon.socket
#
#
#RUN systemctl daemon-reload
# 
#RUN systemctl enable ethoscope_node.service
#RUN systemctl enable ethoscope_backup.service
#RUN systemctl enable ethoscope_video_backup.service


#RUN systemctl daemon-reload
#RUN systemctl enable ethoscope_update_node.service


