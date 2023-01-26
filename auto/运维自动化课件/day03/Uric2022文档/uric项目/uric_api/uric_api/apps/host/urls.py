from django.urls import path, include

from host import views

urlpatterns = [
    path('', views.HostView.as_view()),
]
