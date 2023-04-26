#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

if [ "$CONTAINER" = "web" ] ; then
    python manage.py migrate
    exec python manage.py runserver 0.0.0.0:8000
else 
    celery -A url_shortener worker --loglevel=info
fi
