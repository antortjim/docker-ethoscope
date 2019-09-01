#! /bin/bash

cd /opt/ethoscope-git/node_src/scripts/

echo "Running main server"
/usr/bin/python /opt/ethoscope-git/node_src/scripts/backup_tool.py &

echo "Running backup server"
/usr/bin/python /opt/ethoscope-git/node_src/scripts/server.py &
