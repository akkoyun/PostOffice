#!/bin/bash

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

# Restart WeatherStat Handler
systemctl restart Handler_WeatherStat.service
