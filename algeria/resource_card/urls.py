from django.urls import path
from .views import resources, resource_detail

urlpatterns = [
    path("", resources, name="resourcePage"),
    path("<int:pk>/", resource_detail, name="resource_detail"),
]