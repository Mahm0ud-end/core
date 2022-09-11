#!/bin/sh
echo "---------------- mahmoud changed OS ----------------"
cd ~/core
echo "---------------- Activating Home Assistant venv ----------------"
. ~/core/venv/bin/activate
echo "---------------- Printing the IP-Address ----------------"
ip addr
echo "---------------- Running Home Assistant ----------------"
hass -c ~/core/config
