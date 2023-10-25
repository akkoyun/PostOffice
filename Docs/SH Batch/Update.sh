#!/bin/bash

# Version: 1.0
echo "PostOffice System Git Update..."

# Change Directory to PostOffice
cd /root/PostOffice

# Pull from Git
git pull

# Version: 1.0
echo "PostOffice System Service Restarting..."

# Restart Deamon
systemctl daemon-reload

# Restart PostOffice System Service
systemctl restart PostOffice.service

# Restart RAW Handler
systemctl restart Handler_RAW.service

# Restart Device Handler
systemctl restart Handler_Device.service

# Restart WeatherStat Handler
systemctl restart Handler_WeatherStat.service

# Change Directory to Root
cd ~