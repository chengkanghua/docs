from django.urls import path, include, re_path

from host import views

urlpatterns = [
    # host/
    path('', views.HostModelViewSet.as_view({"get": "list", "post": "create", "delete": "delete_many", "patch": "move_host"})),
    re_path('(?P<pk>\d+)', views.HostModelViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "partial_update"})),

    path('category', views.HostCategoryListAPIView.as_view()),
    path('excel_host', views.HostExcelView.as_view()),
    path("search/", views.HostModelViewSet.as_view({"get": "search"})),
]
