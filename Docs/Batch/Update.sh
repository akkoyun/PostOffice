#!/bin/bash

# Reset Color and Style
reset=$(tput sgr0)

# Set Color and Style
red=$(tput setaf 1)
green=$(tput setaf 2)
yellow=$(tput setaf 3)
blue=$(tput setaf 4)
bold=$(tput bold)
gray=$(tput setaf 240)
underline=$(tput smul)

# Clear Screen
clear

# Version: 1.0
echo "${blue}PostOffice System Update...${reset}"
echo "----------------------------------------------"

# Stop Service
Stop_Service() {

    # Print Message
    echo "${red}Stopping: $1${reset}"
    
    # Stop Service
    sudo systemctl stop "$1"

}

# Start Service
Start_Service() {

    # Print Message
    echo "${green}Starting: $1${reset}"
    
    # Start Service
    sudo systemctl start "$1"

}

# Git Pull
Perform_Git_Pull() {
    
    # Print Message
    echo "${yellow}Git repository updating...${reset}"
    
    git_pull_output=$(git pull 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "${gray}Update Succesful:${reset}"
        echo "${blue}$git_pull_output${reset}"
    else
        echo "${red}Update Fail:${reset}"
        echo "${blue}$git_pull_output${reset}"
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
    sudo cp "$source" "$destination"
    
    # Control copy status
    if [ $? -eq 0 ]; then
        echo "${gray}$source, $destination konumuna kopyalandı.${reset}"
    else
        echo "${red}$source kopyalanamadı.${reset}"
    fi
}

# Change Directory to PostOffice
cd /home/postoffice/PostOffice/src

# Stop Services
Stop_Service PostOffice.service
#Stop_Service Hardware.service
#Stop_Service Handler_RAW.service
#Stop_Service Handler_Parameter.service
#Stop_Service Handler_Payload.service
#Stop_Service Handler_Discord.service
#Stop_Service WeatherStat.service
#Stop_Service PostOffice_Service_Controller.service
Stop_Service nginx.service

# Message
echo "----------------------------------------------"

# Git Pull
Perform_Git_Pull

# Message
echo "----------------------------------------------"

# Table Update
echo "${yellow}Table updating...${reset}"
python3 /home/postoffice/PostOffice/src/Setup/Data_Update.py

# Message
echo "----------------------------------------------"

# Copy Files
echo "${yellow}Updating files...${reset}"

# Copy Service Files
Copy_File "/home/postoffice/PostOffice/src/Docs/Service/PostOffice.service" "/etc/systemd/system/PostOffice.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/Handler_RAW.service" "/etc/systemd/system/Handler_RAW.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/Handler_Parameter.service" "/etc/systemd/system/Handler_Parameter.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/Handler_Payload.service" "/etc/systemd/system/Handler_Payload.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/Handler_Discord.service" "/etc/systemd/system/Handler_Discord.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/PostOffice_Service_Controller.service" "/etc/systemd/system/PostOffice_Service_Controller.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/WeatherStat.service" "/etc/systemd/system/WeatherStat.service"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Service/Hardware.service" "/etc/systemd/system/Hardware.service"

# Copy Nginx Files
Copy_File "/home/postoffice/PostOffice/src/Docs/nginx/PostOffice" "/etc/nginx/sites-available/PostOffice"
Copy_File "/home/postoffice/PostOffice/src/Docs/nginx/nginx.conf" "/etc/nginx/nginx.conf"

# Copy SH Batch Files
Copy_File "/home/postoffice/PostOffice/src/Docs/Batch/Update.sh" "/home/postoffice/"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Batch/Restart.sh" "/root/Restart.sh"
#Copy_File "/home/postoffice/PostOffice/src/Docs/Batch/Service.sh" "/root/Service.sh"

# Message
echo "----------------------------------------------"

# Restart Deamon
sudo systemctl daemon-reload

# Start Services
Start_Service PostOffice.service
#Start_Service Hardware.service
#Start_Service Handler_RAW.service
#Start_Service Handler_Parameter.service
#Start_Service Handler_Payload.service
#Start_Service Handler_Discord.service
#Start_Service WeatherStat.service
#Start_Service PostOffice_Service_Controller.service
Start_Service nginx.service

# Message
echo "----------------------------------------------"

# Change Directory to Root
cd ~