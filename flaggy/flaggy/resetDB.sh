#!/bin/bash

python manage.py dumpdata checkins > temp_data.json
python manage.py reset checkins
python manage.py loaddata temp_data.json