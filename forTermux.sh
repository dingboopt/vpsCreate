#!/bin/bash
apt update
apt install -y git sshpass openssh  python2
pip2 install requests
git clone https://github.com/dingboopt/vpsCreate.git
cd vpsCreate
touch vpn.sh
mkdir ~/.termux
touch ~/.termux/termux.properties
echo "extra-keys = [['ESC','/','-','HOME','UP','END','PGUP'],['TAB','CTRL','ALT','LEFT','DOWN','RIGHT','PGDN']]" > ~/.termux/termux.properties
