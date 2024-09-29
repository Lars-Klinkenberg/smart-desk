# !/bin/bash

echo -e "\e[31m 1/4 Updating ...\e[0m"

sudo apt-get update -y
sudo apt-get upgrade -y

echo -e "\e[31m 2/4 Installing packages ...\e[0m"

sudo apt-get install python3
sudo apt-get install python3-dev
sudo apt install python3-pip
sudo apt-get install -y libmariadb-dev
sudo apt install mariadb-server

echo -e "\e[31m 3/4 Setting up venv ...\e[0m"

cd ..
mkdir logs
sudo apt install python3-venv
python3 -m venv venv

source venv/bin/activate

echo -e "\e[31m 4/4 Installing python librarys ...\e[0m"

pip install pyserial
pip install bottle
pip install rpi.gpio
pip install python-dotenv
pip3 install mariadb
pip install requests