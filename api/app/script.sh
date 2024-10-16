#!/bin/bash

#pytest
pylint src --recursive y -E
if [ $? -gt 0 ]
then
  exit 1
fi

cd src || { echo "Directory 'src' not found."; exit 1; }

#gunicorn --bind 0.0.0.0:8008 config.wsgi
uvicorn main:app --host 0.0.0.0 --port 8080