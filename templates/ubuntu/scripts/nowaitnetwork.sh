#!/bin/sh -eux
systemctl disable systemd-networkd-wait-online.service
systemctl mask systemd-networkd-wait-online.service
