#!/bin/bash

# Renk kodları
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

while true; do
    clear
    # İzlemek istediğiniz servislerin listesi
    services=("PostOffice.service" "Handler_RAW.service" "Handler_Parameter.service" "Handler_WeatherStat.service")

    # Her bir servisi kontrol et
    for service in "${services[@]}"; do
        # Servisin durumunu kontrol et
        systemctl status $service > /dev/null 2>&1

        # Çıkış durumuna göre işlem yap
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}OK${NC} - $service"
        else
            echo -e "${RED}FAIL${NC} - $service"
        fi
    done
    sleep 5
done
