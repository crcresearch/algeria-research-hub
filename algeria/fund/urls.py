from django.urls import path
from .views import funding

urlpatterns = [
    path("", funding, name="fundingOpportunities"),
]