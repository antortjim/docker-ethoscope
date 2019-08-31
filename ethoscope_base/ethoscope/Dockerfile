## This Dockerfile provides a way to virtualize an Arch Linux OS with systemd support in Docker
FROM ethoscope_base 
LABEL maintainer "Antonio Ortega <antonio.ortega@kuleuven.vib.be>"

#######################
## Install packages
########################

## MySQL
RUN mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql

# mysql credentials
# where ethoscope saves temporary local files (e.g. videos)
ARG TARGET_GIT_INSTALL=/opt/ethoscope-git
#ARG UPSTREAM_GIT_REPO=https://github.com/gilestrolab/ethoscope.git


## Getting the ethoscope software
#RUN cd $TARGET_GIT_INSTALL && git remote get-url --all origin

RUN cd $TARGET_GIT_INSTALL/src &&  sed -i "s/'picamera>=1.8',//g" setup.py && pip install -e .[device]

#RUN echo "$TARGET_GIT_INSTALL/$UPDATER_LOCATION_IN_GIT $TARGET_UPDATER_DIR"
#RUN cp $TARGET_GIT_INSTALL/$UPDATER_LOCATION_IN_GIT $TARGET_UPDATER_DIR -r
#RUN cd $TARGET_UPDATER_DIR && cp ethoscope_update.service /etc/systemd/system/ethoscope_update.service
 
RUN echo "bcm2835_wdt" | sudo tee /etc/modules-load.d/bcm2835_wdt.conf
RUN echo "max-load-1 = 24" >> /etc/watchdog.conf
RUN echo "watchdog-device = /dev/watchdog" >> /etc/watchdog.conf
RUN echo "watchdog-timeout = 14" >> /etc/watchdog.conf
RUN echo "realtime = yes" >> /etc/watchdog.conf
RUN echo "priority = 1" >> /etc/watchdog.conf

#RUN pacman -R logrotate --noconfirm
RUN echo "SystemMaxUse=250MB" >> /etc/systemd/journald.conf

# Ethoscope identity
RUN echo "001e27AB5a9e19f94de287e28f789825" >> /etc/machine-id
RUN echo "ETHOSCOPE_001" >> /etc/machine-name
RUN echo "e01" >> /etc/hostname

# Expose port 80 for the ethoscope_node service and 8888 for the updater
EXPOSE 9000 

# Copy the startup script executed with docker exec right after docker run
# This script cannot be passed as ENTRYPOINT because systemd must be for the services to work
COPY startup.sh /root/

# Copy some videos
ARG VIDEO_FOLDER=/ethoscope_data/upload/video/
RUN mkdir -p $VIDEO_FOLDER
COPY videos/*.mp4 $VIDEO_FOLDER/movie.mp4
RUN chmod +x /root/startup.sh

#ENV init /lib/systemd/systemd
#VOLUME [ "/sys/fs/cgroup" ]
#ENTRYPOINT ["/lib/systemd/systemd"]
ENTRYPOINT ["/root/startup.sh"]
