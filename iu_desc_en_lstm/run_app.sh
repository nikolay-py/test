#!/bin/sh

if [[ -f logs/desc_en.log ]]
then
    echo "desc_en.log file exists"
else
    echo "desc_en.log file does not exist"
    mkdir logs
    touch logs/desc_en.log
    echo "desc_en.log file has been created"
fi

python run_app.py