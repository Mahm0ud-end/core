#!/bin/sh
echo "---------------- mahmoud changed OS ----------------"
echo "---------------- apt-get updating ----------------"
sudo apt-get -y update
echo "---------------- Installing build-essential ----------------"
sudo apt -y install build-essential
echo "---------------- Installing python3-venv ----------------"
sudo apt -y install python3-venv
echo "---------------- Installing apt-get packages ----------------"
sudo apt-get -y install python3-pip python3-dev python3-venv autoconf libssl-dev libxml2-dev libxslt1-dev libjpeg-dev libffi-dev libudev-dev zlib1g-dev pkg-config libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev libavfilter-dev ffmpeg
echo "---------------- Installing pip ----------------"
sudo apt-get -y install pip
echo "---------------- Installing ciso8601 ----------------"
sudo pip install ciso8601 --no-binary :all:
cd ~/core
echo "---------------- Running script/setup ----------------"
~/core/script/setup
echo "---------------- Installing raspi-config ----------------"
sudo apt-get -y install raspi-config
echo "---------------- Adding Home Assistant to startup ----------------"
chmod +x ~/core/startHA.sh
(crontab -l ; echo "@reboot  ~/core/startHA.sh")| crontab -
echo "---------------- Enabling stips.local mdns ----------------"
sudo apt -y install avahi-daemon
sudo systemctl restart avahi-daemon
sudo hostnamectl set-hostname stips
sudo systemctl restart avahi-daemon
echo "---------------- Enabling SSH service ----------------"
sudo systemctl enable ssh
sudo systemctl start ssh
echo "---------------- Running Home Assistant starting script ----------------"
~/core/startHA.sh
