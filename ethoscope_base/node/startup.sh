#! /bin/bash

### Enable networktime protocol
systemctl start ntpd.service
systemctl enable ntpd.service
#
## Setting up ssh server
systemctl enable sshd.service
systemctl start sshd.service
#
## to host the bare git repo
systemctl start git-daemon.socket
systemctl enable git-daemon.socket

systemctl daemon-reload

systemctl enable ethoscope_node.service
systemctl enable ethoscope_backup.service
systemctl enable ethoscope_video_backup.service


systemctl start ethoscope_node.service
systemctl start ethoscope_backup.service
systemctl start ethoscope_video_backup.service

systemctl daemon-reload
systemctl enable ethoscope_update_node.service
systemctl start ethoscope_update_node.service
