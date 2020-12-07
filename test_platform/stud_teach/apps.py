from configparser import ConfigParser
from threading import Thread

from django.apps import AppConfig
from django.core import signals

# from stud_teach.admin import send_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread
import datetime
import smtplib
import croniter
from django.utils import timezone



config = ConfigParser()
config.read("config.ini")
smtp = config["smtp"]

class StudTeachConfig(AppConfig):
    name = 'stud_teach'
