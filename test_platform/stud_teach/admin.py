import datetime
import smtplib
from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

import croniter
from django.contrib import admin
from django.utils import timezone
from stud_teach.models import Student, Teacher, Question, Test, ResultTest

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(ResultTest)


config = ConfigParser()
config.read("config.ini")
smtp = config["smtp"]


# def send_email():
#     """
#     отправка статистики пройденных тестов за день в указанное время
#     """
#     cron = croniter.croniter(smtp["time"], datetime.datetime.now())
#     send_time = cron.get_next(datetime.datetime)
#
#     while True:
#         if datetime.datetime.now() == send_time:
#             results = ResultTest.objects.filter(at__lt=timezone.now(), at__gt=timezone.now() - timezone.timedelta(days=1))
#             filename = f"results_{datetime.datetime.now().date()}.csv"
#             with open(f"files/{filename}", "w") as file:
#                 file.write("Название теста;баллы;студент\n")
#                 for result in results:
#                     file.write(result.test.title + ";" + str(result.passed) + ";" + result.student.username + "\n")
#             msg = MIMEMultipart()
#             msg["From"] = smtp["login"]
#             msg["To"] = smtp["send_to"]
#             msg["Subject"] = "Статистика пройденных тестов за прошедший день"
#             with open(f"files/{filename}", "r") as fn:
#                 file = MIMEText(fn.read())
#                 file.add_header('Content-Disposition', 'file', filename=filename)
#             msg.attach(file)
#
#             post = smtplib.SMTP(smtp["host"], smtp["port"])
#             post.starttls()
#             post.login(smtp["login"], smtp["password"])
#             post.send_message(msg)
#             post.quit()
#             send_time = cron.get_next(datetime.datetime)


# email_task = Thread(target=send_email)
# email_task.start()
