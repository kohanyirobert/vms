#!/bin/sh -eux
chmod -x /etc/update-motd.d/*
wget -O /etc/motd $FILE_SERVER_URL/motd
