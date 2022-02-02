#!/bin/bash

DIR=/opt/muya-startup/muya-startup.d
if [[ -d "$DIR" && "${MUYA_STARTUP:-true}" == "true" ]]; then
  /bin/run-parts --verbose --exit-on-error "$DIR"
fi

if [[ "${MUYA_DEVSERVER:-false}" == "true" ]]; then
    exec python manage.py runserver 0.0.0.0:$PORT
else
    exec gunicorn --config file:/opt/clips/clump/gunicorn.py clump.wsgi
fi
