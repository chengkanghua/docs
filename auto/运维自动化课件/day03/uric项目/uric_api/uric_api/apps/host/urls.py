from django.urls import path, include

from host import views

urlpatterns = [
    path('list', views.HostView.as_view()),
]
