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

# Restart Power Handler
systemctl restart Handler_Power.service

# Restart Info Handler
systemctl restart Handler_Info.service

# Restart IoT Handler
systemctl restart Handler_IoT.service

# Change Directory to Root
cd ~