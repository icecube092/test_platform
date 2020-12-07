from threading import Thread

from stud_teach.admin import send_email

if __name__ == '__main__':
    email_task = Thread(target=send_email)
    email_task.start()