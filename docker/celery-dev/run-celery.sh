#!/bin/bash

if [[ "${MUYA_DEVSERVER:-false}" == "true" ]]; then
    exec celery -A muya_wce worker -l INFO
else
    exec celery -A muya_wce worker -l INFO
fi
