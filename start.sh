#!/bin/bash

# Optional: install Chrome for Selenium if needed
apt-get update
apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome*.deb; apt-get -fy install

# Run Streamlit on the Render-assigned port
streamlit run app.py --server.port=$PORT --server.enableCORS=false
