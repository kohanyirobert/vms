#!/bin/sh -eux
for country_code in us hu pl
do
  keyboard_file=keyboard.$country_code
  console_setup_file=console-setup.$country_code
  wget -O /etc/default/$keyboard_file $FILE_SERVER_URL/default/$keyboard_file
  wget -O /etc/default/$console_setup_file $FILE_SERVER_URL/default/$console_setup_file
done

wget -O /usr/bin/chlang $FILE_SERVER_URL/chlang
chmod +x /usr/bin/chlang
