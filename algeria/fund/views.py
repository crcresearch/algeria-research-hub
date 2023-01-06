from django.shortcuts import render
from .models import Fund

# Create your views here.
def funding(request):
    funding = Fund.objects.order_by("posted_date")
    return render(request, "pages/fundingOpportunities.html", {"funding": funding})