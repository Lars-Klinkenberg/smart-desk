sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install python3
sudo apt-get install python3-dev
sudo apt install python3-pip
sudo apt-get install -y libmariadb-dev
sudo apt install mariadb-server

sudo apt install python3-venv
python3 -m venv venv
source ./venv/bin/activate

pip install pyserial
pip install bottle
pip install rpi.gpio
pip install python-dotenv
pip3 install mariadb

python main.py