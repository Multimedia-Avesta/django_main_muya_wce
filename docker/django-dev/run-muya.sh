#!/bin/bash

DIR=/opt/muya-startup/muya-startup.d
if [[ -d "$DIR" && "${MUYA_STARTUP:-true}" == "true" ]]; then
  /bin/run-parts --verbose --exit-on-error "$DIR"
fi

if [[ "${MUYA_DEVSERVER:-false}" == "true" ]]; then
    exec python manage.py runserver 0.0.0.0:$PORT
else
    exec uwsgi --ini /opt/muya-startup/muya_uwsgi.ini
fi
