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
echo "${red}${bold}PostOffice System Update...${reset}"

# Stop Service
Stop_Service() {

    # Print Message
    echo "${YELLOW}Stopping: $1${RESET}"
    
    # Stop Service
    systemctl stop "$1"

}

# Start Service
Start_Service() {

    # Print Message
    echo "${YELLOW}Starting: $1${RESET}"
    
    # Start Service
    systemctl start "$1"

}

# Git Pull
Perform_Git_Pull() {
    
    # Print Message
    echo "${YELLOW}Git repository updating...${RESET}"
    
    git_pull_output=$(git pull 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "${GREEN}Update Succesful:${RESET}"
        echo "${BLUE}$git_pull_output${RESET}"
    else
        echo "${RED}Update Fail:${RESET}"
        echo "${BLUE}$git_pull_output${RESET}"
    fi
}

# Copy File
Copy_File() {

    # Declare variables
    source=$1
    destination=$2

    # Control source file
    if [ ! -f "$source" ]; then
        echo "${RED}Kaynak dosya bulunamadı: $source${RESET}"
        return 1
    fi

    # Copy file
    cp "$source" "$destination"
    
    # Control copy status
    if [ $? -eq 0 ]; then
        echo "${GREEN}$source, $destination konumuna kopyalandı.${RESET}"
    else
        echo "${RED}$source kopyalanamadı.${RESET}"
    fi
}

# Change Directory to PostOffice
cd /root/PostOffice

# Stop Services
Stop_Service PostOffice.service
Stop_Service Handler_RAW.service

# Git Pull
Perform_Git_Pull

# Copy Service Files
Copy_File "~/PostOffice/Docs/Service/PostOffice.service" "/etc/systemd/system/PostOffice.service"
Copy_File "~/PostOffice/Docs/Service/Handler_RAW.service" "/etc/systemd/system/Handler_RAW.service"

# Copy SH Batch Files
Copy_File "~/PostOffice/Docs/Batch/Update.sh" "/root/Update.sh"
Copy_File "~/PostOffice/Docs/Batch/Restart.sh" "/root/Restart.sh"
Copy_File "~/PostOffice/Docs/Batch/Service.sh" "/root/Service.sh"

# Message
echo "${green}${bold}PostOffice System Service Restarting...${reset}"

# Restart Deamon
systemctl daemon-reload

# Start Services
Start_Service PostOffice.service
Start_Service Handler_RAW.service

# Change Directory to Root
cd ~