from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("app", views.ReleaseAPIView, "app")
router.register("gitlab", views.GitlabAPIView, "gitlab")
router.register("jenkins", views.JenkinsAPIView, "jenkins")

urlpatterns = [

] + router.urls
