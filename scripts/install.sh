# !/bin/bash

echo -e "\e[31m 1/7 Updating ...\e[0m"

sudo apt-get update -y
sudo apt-get upgrade -y

echo -e "\e[31m 2/7 Installing packages ...\e[0m"

sudo apt-get install python3
sudo apt-get install python3-dev
sudo apt install python3-pip
sudo apt-get install -y libmariadb-dev
sudo apt install mariadb-server

echo -e "\e[31m 3/7 Setting up venv ...\e[0m"

cd ..
mkdir logs
sudo apt install python3-venv
python3 -m venv venv

source venv/bin/activate

echo -e "\e[31m 4/7 Installing python librarys ...\e[0m"

pip install pyserial
pip install bottle
pip install rpi.gpio
pip install python-dotenv
pip3 install mariadb
pip install requests

echo -e "\e[31m 5/7 Linking systemd files ...\e[0m"

sudo ln -s /home/raspberry/smart-desk/smart-desk/systemd/api-controller.service /etc/systemd/system/api-controller.service
sudo ln -s /home/raspberry/smart-desk/smart-desk/systemd/desk-controller.service /etc/systemd/system/desk-controller.service

echo -e "\e[31m 5/7 Start services on startup ...\e[0m"

sudo systemctl daemon-reload
sudo systemctl enable api-controller.service
sudo systemctl enable desk-controller.service

echo -e "\e[31m 5/7 Starting api-controller and desk-controller service manually ...\e[0m"
sudo systemctl start api-controller.service
sudo systemctl start desk-controller.service