from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from stud_teach.models import Test

from stud_teach.models import Teacher, Student

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


def test_page(request):
    test_id = request.GET.get("test_id")
    if test_id:
        try:
            user = Teacher.objects.get(id=request.user.id)
        except Teacher.DoesNotExist:
            try:
                user = Student.objects.get(id=request.user.id)
            except Student.DoesNotExist:
                user = AnonymousUser()
        test = get_object_or_404(Test, pk=test_id)
        questions = test.questions.all()
        if enter and request.method == "POST":
            if request.user.is_authenticated:
                if user.username in pending:
                    project.users_pending.remove(user)
                elif user.username in members:
                    project.members.remove(user)
                else:
                    project.users_pending.add(user)
                return HttpResponseRedirect(
                    f"/projects/?project_id={test_id}")
            else:
                return HttpResponseRedirect("/login/")
        return render(request, "projects/project_page.html",
                      {"project": project, "members": members,
                       "comments": comments, "pending": pending,
                       "is_member": is_member, "is_owner": is_owner})
    else:
        return HttpResponseRedirect("../tests/1")