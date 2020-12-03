from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

# Create your views here.
from stud_teach.models import Test

from stud_teach.models import Teacher, Student

from stud_teach.forms import PassedTestForm

items_on_page = 10


def tests_list(request, page: int):
    """
    страница со списком проектов
    """
    count_tests = page * items_on_page
    tests = Test.objects.all()[count_tests - items_on_page: count_tests]
    prev_page = page - 1 or 1
    next_page = page + 1 if len(tests) == items_on_page else page
    return render(request, "tests_list.html",
                  {"tests": tests, "page": page, "prev_page": prev_page, "next_page": next_page})


class TestPage(View):
    """
    страница с тестом
    """
    def get(self, request):
        test_id = request.GET.get("test_id")
        test = get_object_or_404(Test, pk=test_id)
        is_teacher = False
        is_student = False
        if test_id:
            try:
                user = Teacher.objects.get(id=request.user.id)
                is_teacher = True
            except Teacher.DoesNotExist:
                try:
                    user = Student.objects.get(id=request.user.id)
                    is_student = True
                except Student.DoesNotExist:
                    user = AnonymousUser()
            students_pass = Student.objects.filter(done_tests=test.id)
            results = {}
            for student in students_pass:
                result = student.resulttest_set.get(test=test)
                results.update({student: result})
            questions = test.questions.all()
            passed = 0
            if is_student:
                try:
                    user.done_tests.get(id=test_id)
                    passed = user.resulttest_set.get(test=test).passed
                except Test.DoesNotExist:
                    passed = 0
            return render(request, "test_page.html",
                          {"results": results, "questions": questions, "is_teacher": is_teacher,
                           "is_student": is_student, "passed": passed, "test": test})
        else:
            return HttpResponseRedirect("../tests/1")

    def post(self, request):
        test_id = request.GET.get("test_id")
        if test_id:
            try:
                user = Student.objects.get(id=request.user.id)
            except Student.DoesNotExist:
                return HttpResponse("Вы не студент")
            print(request.POST)
            return HttpResponseRedirect(f"/tests/?test_id={test_id}")
        else:
            return HttpResponseRedirect("../tests/1")