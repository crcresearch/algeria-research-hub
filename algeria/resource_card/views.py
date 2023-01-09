from django.shortcuts import render
from .models import Resource
# Create your views here.
def resources(request):
    resources = Resource.objects.order_by("title")
    return render(request, "pages/resourcePage.html", {"resources": resources})