#!/bin/bash

if [[ "${MUYA_DEVSERVER:-false}" == "true" ]]; then
    exec celery --app muya_wce worker --loglevel INFO
else
    exec celery --app muya_wce worker --loglevel INFO --pool gevent --concurrency 500 --uid muya
fi
