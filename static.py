#!/usr/bin/env python
import os
# To import anything under django.*, we must set this variable.
os.environ['DJANGO_SETTINGS_MODULE'] = 'flaggy.settings'
# Import the admin module. The media directory is right under it!
import django.contrib.admin
# Retrieve the absolute path of the admin module.
admindir = os.path.dirname(django.contrib.admin.__file__)
# Add /media behind it.
mediadir = os.path.join(admindir, 'media')
# Compute the path of the symlink under the static directory.
staticlink = os.path.join('static', 'admin_media')
# If the link already exists, delete it.
if os.path.islink(staticlink):
    os.unlink(staticlink)
# Install the correct link.
os.symlink(mediadir, staticlink)
