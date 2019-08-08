## This Dockerfile provides a way to virtualize an Arch Linux OS with systemd support in Docker
FROM archlinux/base
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
RUN git clone --bare https://github.com/gilestrolab/ethoscope.git /srv/git/ethoscope.git


## The node software
## https://qgeissmann.gitbooks.io/ethoscope-manual/building-and-installation/node.html#the-node-software
# variables
RUN TARGET_UPDATER_DIR=/opt/ethoscope_updater
RUN TARGET_GIT_INSTALL=/opt/ethoscope-git

#Create a local working copy from the bare repo on node
RUN echo 'Installing ethoscope package'
RUN git clone /srv/git/ethoscope.git /opt/ethoscope-git


## IMPORTANT this is if you want to work on the "dev" branch otherwise, you are using "master"
RUN cd /opt/ethoscope-git &&  git checkout -b python3.7 && git pull origin python3.7
#
## we install with pip
RUN cd /opt/ethoscope-git/node_src && pip install -e .
##
### we create a symbolic link of the updated in the proper location
RUN ln -s /opt/ethoscope-git/scripts/ethoscope_updater /opt/ethoscope_updater
