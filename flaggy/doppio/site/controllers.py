import hashlib
import smtplib

from json import dumps
from doppio.models import User, FollowPending, Follow, CheckIn
from datetime import datetime
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from doppio.api.emails import emails