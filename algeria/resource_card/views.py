from django.shortcuts import render, get_object_or_404
from .models import Resource
# Create your views here.
def resources(request):
    resources = Resource.objects.order_by("title")
    return render(request, "pages/resourcePage.html", {"resources": resources})

def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, "resource/resourceDetail.html", {"resource": resource})