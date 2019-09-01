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
#RUN pip install systemd


#################################
## Download ethoscope software
##################################

#ARG UPSTREAM_GIT_REPO_HOST=upstream
#ARG UPSTREAM_GIT_REPO=/ethoscope_copy
ARG UPSTREAM_GIT_REPO=https://gitlab.com/antortjim/ethoscope_upstream.git
ARG UPDATER_LOCATION_IN_GIT=scripts/ethoscope_updater
ARG LOCAL_BARE_PATH=/srv/git/ethoscope.git
ARG TARGET_UPDATER_DIR=/opt/ethoscope_updater
ARG TARGET_GIT_INSTALL=/opt/ethoscope-git

## Copy a local version of the repo to $UPSTREAM_GIT_REPO
## This is the version that the images will make use of\
## Any modifications to the software in $UPSTREAM_GIT_REPO_HOST
## are propagated to the images!

#COPY $UPSTREAM_GIT_REPO_HOST  $UPSTREAM_GIT_REPO
RUN mkdir -p /srv/git

#ARG USER=antortjim
#ARG REPO=ethoscope_upstream
#ARG BRANCH=python3.7
#ADD https://gitlab.com/api/v4/projects//$REPO/git/refs/heads/$BRANCH version.json
#RUN git clone --bare -b$BRANCH https://gitlab.com/$USER/$REPO.git $LOCAL_BARE_PATH

## Clone the git repo in the /srv/git dir as bare
## Trick to force Docker to always query Gitlab: http://dev.im-bot.com/docker-select-caching/
## This is required in case there are updates in the repo
ARG CACHEBUST=1
RUN git clone --bare $UPSTREAM_GIT_REPO $LOCAL_BARE_PATH



## Clone from the bare repo to TARGET_GIT_INSTALL
RUN git clone $LOCAL_BARE_PATH $TARGET_GIT_INSTALL


## IMPORTANT this is if you want to work on a specific branch
RUN cd $TARGET_GIT_INSTALL &&  git checkout python3.7 && git pull origin python3.7

## Define an environment variable available in all ethoscope containers
## The definition will change the program's behavior to make it aware
## of it running in a container
ENV DOCKER_CONTAINER Yes

