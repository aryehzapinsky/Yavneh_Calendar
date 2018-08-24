#!/usr/bin/env bash

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
rm get-pip.py

sudo pip install --upgrade virtualenv
sudo apt-get install git



git clone https://github.com/aryehzapinsky/Yavneh_Calendar.git
cd Yavneh_Calendar/
virtualenv --python python3 calendar-env
source calendar-env/bin/activate
pip install -r requirements.txt

# put client_secret.json in folder
# when run from google cloud use --noauth_local_webserver --> ./create_events_from_zmanim.py 08/27/18 08/28/18 --noauth_local_webserver
