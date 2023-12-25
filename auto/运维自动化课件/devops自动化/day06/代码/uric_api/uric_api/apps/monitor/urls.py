from django.urls import path, re_path
from . import  views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("param", views.MonitorParamViewSet, basename="param")
router.register("host", views.MonitorHostViewSet, basename="host")

urlpatterns = [
    path("notif/", views.NotificationTypeAPIView.as_view()),
] + router.urls