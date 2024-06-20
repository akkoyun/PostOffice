#!/bin/bash

for i in {1..4}
do
    /home/postoffice/PostOffice/PostOffice_ENV/bin/python3 /home/postoffice/PostOffice/src/Consumer/DataHandler.py &
done

wait
