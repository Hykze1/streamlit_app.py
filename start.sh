#!/bin/bash

# Install Chrome
apt-get update
apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome*.deb; apt-get -fy install

# Start your app
streamlit run app.py
