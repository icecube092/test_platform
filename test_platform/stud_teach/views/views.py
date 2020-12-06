from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from stud_teach.models import ResultTest, Teacher, Student, Test

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
        if test_id:
            test = get_object_or_404(Test, pk=test_id)
            is_teacher = False
            is_student = False
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
            passed = -1
            if is_student:
                try:
                    user.done_tests.get(id=test_id)
                    passed = user.resulttest_set.get(test=test).passed
                except Test.DoesNotExist:
                    passed = -1
            return render(request, "test_page.html",
                          {"results": results, "questions": questions, "is_teacher": is_teacher,
                           "is_student": is_student, "passed": passed, "test": test})
        else:
            return HttpResponseRedirect(reverse("tests_list", args=[1]))

    def post(self, request):
        test_id = request.GET.get("test_id")
        if test_id:
            is_teacher = False
            is_student = False
            try:
                user = Teacher.objects.get(id=request.user.id)
                is_teacher = True
            except Teacher.DoesNotExist:
                try:
                    user = Student.objects.get(id=request.user.id)
                    is_student = True
                except Student.DoesNotExist:
                    user = AnonymousUser()
            if is_student:
                test = get_object_or_404(Test, pk=test_id)
                right_answers = tuple(question.right for question in test.questions.all())
                user_result = 0
                answers = request.POST.dict()
                answers.pop("csrfmiddlewaretoken")
                for key, right in zip(answers, right_answers):
                    if answers[key][0] == right:
                        user_result += 1
                user.done_tests.add(test)
                result = ResultTest()
                result.test = test
                result.passed = user_result
                result.student = user
                result.save()
            elif is_teacher:
                reset_id = request.GET.get("reset_id")
                if reset_id:
                    student = Student.objects.get(id=reset_id)
                    test = Test.objects.get(id=test_id)
                    student.done_tests.remove(test)
                    ResultTest.objects.filter(student=student, test=test).delete()
            return HttpResponseRedirect(f"{reverse('test_page')}?test_id={test_id}")
        else:
            return HttpResponseRedirect(reverse("tests_list", args=[1]))