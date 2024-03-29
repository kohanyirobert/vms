#!/bin/sh -eux
apt-get -y install python mininet openvswitch-testcontroller
systemctl stop openvswitch-testcontroller
systemctl disable openvswitch-testcontroller
systemctl enable openvswitch-switch
systemctl start openvswitch-switch
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
python get-pip.py
pip install ipaddress
rm -rf get-pip.py
