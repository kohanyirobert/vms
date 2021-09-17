#!/bin/sh -eux
systemctl disable motd-news.service
systemctl disable motd-news.timer
chmod -x /etc/update-motd.d/*
wget -O /etc/motd $FILE_SERVER_URL/motd
