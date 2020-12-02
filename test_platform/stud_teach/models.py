from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=250)
    option_1 = models.CharField(max_length=100, name="1")
    option_2 = models.CharField(max_length=100, name="2")
    option_3 = models.CharField(max_length=100, name="3")
    option_4 = models.CharField(max_length=100, name="4")
    OPTIONS = (
        ("1", option_1.name),
        ("2", option_2.name),
        ("3", option_3.name),
        ("2", option_4.name)
    )
    right = models.CharField(max_length=10, choices=OPTIONS, name="Правильный ответ")

    def __str__(self):
        return self.text


class Test(models.Model):
    title = models.CharField(max_length=100, default="Тест")
    questions = models.ForeignKey(Question, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Student(User):
    done_tests = models.ManyToManyField(Test)
    avatar = models.ImageField(blank=True)
    phone = models.CharField(max_length=11, blank=True)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.username


class Teacher(User):
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.username