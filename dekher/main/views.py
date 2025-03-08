from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from fund.models import Fund
# Create your views here.


def home_view(request: HttpRequest):

    funds = Fund.objects.filter(owner = request.user)
    return render(request, 'home.html', context={'funds': funds})