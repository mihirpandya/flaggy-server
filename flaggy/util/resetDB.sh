#!/bin/bash

python ../manage.py dumpdata checkins > backup_data.json
python ../manage.py reset doppio
python ../manage.py loaddata temp_data.json