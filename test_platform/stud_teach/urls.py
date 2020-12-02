from django.urls import path

from stud_teach.views import views

urlpatterns = [
    path('', views.test_page, name="test_page"),
    path('<int:page>/', views.tests_list, name="tests_list")
]