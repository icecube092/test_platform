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

    def ready(self):
        signals.request_started.connect(send_mail, sender=self)


def send_mail(sender, **kwargs):
    email_task = Thread(target=send_email)
    email_task.start()

def send_email():
    """
    отправка статистики пройденных тестов за день в указанное время
    """
    from stud_teach.models import ResultTest
    cron = croniter.croniter(smtp["time"], datetime.datetime.now())
    send_time = cron.get_next(datetime.datetime)

    while True:
        print("hello")
        if datetime.datetime.now() == send_time:
            results = ResultTest.objects.filter(at__lt=timezone.now(), at__gt=timezone.now() - timezone.timedelta(days=1))
            filename = f"results_{datetime.datetime.now().date()}.csv"
            with open(f"files/{filename}", "w") as file:
                file.write("Название теста;баллы;студент\n")
                for result in results:
                    file.write(result.test.title + ";" + str(result.passed) + ";" + result.student.username + "\n")
            msg = MIMEMultipart()
            msg["From"] = smtp["login"]
            msg["To"] = smtp["send_to"]
            msg["Subject"] = "Статистика пройденных тестов за прошедший день"
            with open(f"files/{filename}", "r") as fn:
                file = MIMEText(fn.read())
                file.add_header('Content-Disposition', 'file', filename=filename)
            msg.attach(file)

            post = smtplib.SMTP(smtp["host"], smtp["port"])
            post.starttls()
            post.login(smtp["login"], smtp["password"])
            post.send_message(msg)
            post.quit()
            send_time = cron.get_next(datetime.datetime)