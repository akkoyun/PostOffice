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
echo "${blue}${underline}PostOffice System Update...${reset}"
echo "----------------------------------------------"

# Stop Service
Stop_Service() {

    # Print Message
    echo "${red}Stopping: $1${reset}"
    
    # Stop Service
    systemctl stop "$1"

}

# Start Service
Start_Service() {

    # Print Message
    echo "${green}Starting: $1${reset}"
    
    # Start Service
    systemctl start "$1"

}

# Git Pull
Perform_Git_Pull() {
    
    # Print Message
    echo "${yellow}Git repository updating...${reset}"
    
    git_pull_output=$(git pull 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "${green}Update Succesful:${reset}"
        echo "${BLUE}$git_pull_output${reset}"
    else
        echo "${red}Update Fail:${reset}"
        echo "${BLUE}$git_pull_output${reset}"
    fi
}

# Copy File
Copy_File() {

    # Declare variables
    source=$1
    destination=$2

    # Control source file
    if [ ! -f "$source" ]; then
        echo "${red}Kaynak dosya bulunamadı: $source${reset}"
        return 1
    fi

    # Copy file
    cp "$source" "$destination"
    
    # Control copy status
    if [ $? -eq 0 ]; then
        echo "${green}$source, $destination konumuna kopyalandı.${reset}"
    else
        echo "${red}$source kopyalanamadı.${reset}"
    fi
}

# Change Directory to PostOffice
cd /root/PostOffice

# Stop Services
Stop_Service PostOffice.service
Stop_Service Handler_RAW.service
Stop_Service Handler_Parameter.service
Stop_Service Handler_Payload.service
Stop_Service PostOffice_Service_Controller.service

# Message
echo "----------------------------------------------"

# Git Pull
Perform_Git_Pull

# Message
echo "----------------------------------------------"

# Table Update
echo "${yellow}Table updating...${reset}"
python3 /root/PostOffice/Setup/Data_Update.py

# Message
echo "----------------------------------------------"

# Copy Service Files
Copy_File "/root/PostOffice/Docs/Service/PostOffice.service" "/etc/systemd/system/PostOffice.service"
Copy_File "/root/PostOffice/Docs/Service/Handler_RAW.service" "/etc/systemd/system/Handler_RAW.service"
Copy_File "/root/PostOffice/Docs/Service/Handler_Parameter.service" "/etc/systemd/system/Handler_Parameter.service"
Copy_File "/root/PostOffice/Docs/Service/Handler_Payload.service" "/etc/systemd/system/Handler_Payload.service"
Copy_File "/root/PostOffice/Docs/Service/PostOffice_Service_Controller.service" "/etc/systemd/system/PostOffice_Service_Controller.service"

# Copy Admin Files
cd /root
rm -r /var/www/admin/*
cp -r /root/PostOffice/Admin/* /var/www/admin/

# Copy SH Batch Files
Copy_File "/root/PostOffice/Docs/Batch/Update.sh" "/root/Update.sh"
Copy_File "/root/PostOffice/Docs/Batch/Restart.sh" "/root/Restart.sh"
Copy_File "/root/PostOffice/Docs/Batch/Service.sh" "/root/Service.sh"

# Message
echo "----------------------------------------------"

# Message
echo "${green}${bold}PostOffice System Service Restarting...${reset}"

# Restart Deamon
systemctl daemon-reload

# Start Services
Start_Service PostOffice.service
Start_Service Handler_RAW.service
Start_Service Handler_Parameter.service
Start_Service Handler_Payload.service
Start_Service PostOffice_Service_Controller.service

# Message
echo "----------------------------------------------"

# Change Directory to Root
cd ~