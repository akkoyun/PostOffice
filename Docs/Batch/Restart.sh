#!/bin/bash

# Reset Color and Style
reset=$(tput sgr0)

# Set Color and Style
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
bold=$(tput bold)
underline=$(tput smul)

# Clear Screen
clear

# Version: 1.0
echo "${blue}${underline}PostOffice System Restart...${reset}"
echo "----------------------------------------------"

# Restart Service
Restart_Service() {

    # Print Message
    echo "${green}Restarting: $1${reset}"
    
    # Start Service
    systemctl restart "$1"

}

# Message
echo "${green}${bold}PostOffice System Service Restarting...${reset}"

# Restart Services
Restart_Service PostOffice.service
Restart_Service Handler_RAW.service
Restart_Service Handler_Parameter.service
Restart_Service Handler_Payload.service

# Message
echo "----------------------------------------------"
