import json
import os

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from ads.models import Ad, Category
from users.models import Location, User


def index(request):
    return JsonResponse({"status": "ok"}, status=200)
