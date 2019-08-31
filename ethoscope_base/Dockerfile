## This Dockerfile provides a way to virtualize the basic Docker OS.
## Two extra Dockerfiles can use the resulting image to create a node and an ethoscope image
FROM archlinux/base
LABEL maintainer "Antonio Ortega <antonio.ortega@kuleuven.vib.be>"

#################################
## Update arch linux
##################################
RUN pacman -Syu --noconfirm
RUN pacman -Syu --noconfirm --debug

#################################
## Dependiencies and utilities
##################################

# tools for developers
RUN pacman -S base-devel git gcc-fortran rsync wget fping --noconfirm --needed

# utilities
RUN pacman -S ntp bash-completion openssh --noconfirm --needed

#so we can set up a dns
RUN pacman -S dnsmasq --noconfirm --needed

# pre-installing dependencies will save compiling time on python packages
RUN pacman -S python2-pip python2-numpy python2-bottle python2-pyserial mysql-python python2-netifaces python2-cherrypy python2-futures ipython2 python2-scipy python2-pillow --noconfirm --needed

# install python3
RUN pacman -Sy --noconfirm python python-pip
RUN pip install bottle

# mariadb
RUN pacman -S mariadb --noconfirm --needed

# setup Wifi dongle
RUN pacman -S wpa_supplicant --noconfirm --needed
RUN pacman -S libev --noconfirm --needed
RUN pacman -S base-devel git gcc-fortran rsync wget --noconfirm --needed
RUN pacman -S ntp bash-completion --noconfirm --needed

# Install vim
RUN pacman -Sy --noconfirm vim


## Stuff required only by devices
RUN pacman -S --noconfirm hdf5
RUN pacman -S --noconfirm opencv
RUN pacman -S --noconfirm gtk3
RUN pip install h5py==2.6.0

# video processing / image analysis tools
RUN pacman -S eigen mplayer ffmpeg gstreamer mencoder --noconfirm --needed
RUN pacman -S ifplugd  --noconfirm --needed
RUN pacman -S macchanger --noconfirm --needed
RUN pip install zeroconf

# Install systemd module to be able to easily log to syslog
RUN pip install systemd


#################################
## Download ethoscope software
##################################

ARG UPSTREAM_GIT_REPO_HOST=upstream
ARG UPSTREAM_GIT_REPO=/ethoscope_copy
ARG UPDATER_LOCATION_IN_GIT=scripts/ethoscope_updater
ARG LOCAL_BARE_PATH=/srv/git/ethoscope.git
ARG TARGET_UPDATER_DIR=/opt/ethoscope_updater
ARG TARGET_GIT_INSTALL=/opt/ethoscope-git

## Copy a local version of the repo to $UPSTREAM_GIT_REPO
## This is the version that the images will make use of\
## Any modifications to the software in $UPSTREAM_GIT_REPO_HOST
## are propagated to the images!

COPY $UPSTREAM_GIT_REPO_HOST  $UPSTREAM_GIT_REPO
RUN mkdir -p /srv/git
## Clone the git repo in the /srv/git dir as bare
RUN git clone --bare $UPSTREAM_GIT_REPO $LOCAL_BARE_PATH
## Clone from the bare repo to TARGET_GIT_INSTALL
RUN git clone $LOCAL_BARE_PATH $TARGET_GIT_INSTALL


## IMPORTANT this is if you want to work on a specific branch
RUN cd $TARGET_GIT_INSTALL &&  git checkout python3.7 && git pull origin python3.7

### we create a symbolic link of the updated in the proper location
RUN ln -s $TARGET_GIT_INSTALL/scripts/ethoscope_updater $TARGET_UPDATER_DIR

### Copy the node services
#RUN cd $TARGET_GIT_INSTALL/scripts && cp ./ethoscope_node.service /etc/systemd/system/ethoscope_node.service && cp ./ethoscope_backup.service /etc/systemd/system/ethoscope_backup.service && cp ./ethoscope_video_backup.service /etc/systemd/system/ethoscope_video_backup.service
#
### Copy the device service
#RUN cp $TARGET_GIT_INSTALL/scripts/ethoscope_device.service /etc/systemd/system/ethoscope_device.service
#
### Copy the node update service
#RUN cd $TARGET_UPDATER_DIR && cp ethoscope_update_node.service /etc/systemd/system/ethoscope_update_node.service
#
### Copy the device update service
#RUN cd $TARGET_GIT_INSTALL/$UPDATER_LOCATION_IN_GIT && cp ethoscope_update.service /etc/systemd/system/ethoscope_update.service
#
### Make sure the services refer to the source folder as ethoscope-git
#RUN cd /etc/systemd/system && sed -i 's/ethoscope-node/ethoscope-git/' ethoscope_*.service && sed -i 's/ethoscope-device/ethoscope-git/' ethoscope_*.service

ENV DOCKER_CONTAINER Yes


#ENV init /lib/systemd/systemd
#VOLUME [ "/sys/fs/cgroup" ]
#ENTRYPOINT ["/lib/systemd/systemd"]
ENTRYPOINT ["sleep", "6000"]

