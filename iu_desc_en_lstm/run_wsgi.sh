#!/bin/sh

read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1]}
}

GUNICORN_TIMEOUT=$(read_var GUNICORN_TIMEOUT .env)

if [[ -f logs/desc_en.log ]]
then
  echo "desc_en.log file exists"
else
  echo "desc_en.log file does not exits"
  mkdir logs
  touch logs/desc_en.log
  echo "desc_en.log file has been created"
fi

gunicorn --workers=4 --timeout=${GUNICORN_TIMEOUT} --bind 0.0.0.0:8000 wsgi:app
