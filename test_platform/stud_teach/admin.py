from django.contrib import admin

# Register your models here.
from stud_teach.models import Student, Teacher, Question, Test, ResultTest

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(ResultTest)