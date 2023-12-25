from django.urls import path, re_path
from . import views

urlpatterns = [
    path('periods/', views.PeriodView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    re_path('tasks/(?P<pk>\d+)/', views.TaskDetaiView.as_view()),
]