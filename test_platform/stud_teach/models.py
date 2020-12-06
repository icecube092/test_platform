import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=250)
    option_1 = models.CharField(max_length=100, verbose_name="Вариант 1")
    option_2 = models.CharField(max_length=100, verbose_name="Вариант 2")
    option_3 = models.CharField(max_length=100, verbose_name="Вариант 3")
    option_4 = models.CharField(max_length=100, verbose_name="Вариант 4")
    OPTIONS = (
        ("1", option_1.verbose_name),
        ("2", option_2.verbose_name),
        ("3", option_3.verbose_name),
        ("4", option_4.verbose_name)
    )
    right = models.CharField(max_length=10, choices=OPTIONS, verbose_name="Правильный ответ")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Test(models.Model):
    title = models.CharField(max_length=100, default="Тест")
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Student(User):
    avatar = models.ImageField(blank=True, upload_to=f"users/{datetime.datetime.now()}")
    phone = models.CharField(max_length=11, blank=True)
    done_tests = models.ManyToManyField(Test, related_name="done_tests", blank=True)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.username


class ResultTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    passed = models.IntegerField(default=0)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return f"{self.test.title} - {self.student.username}"

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

class Teacher(User):
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.username