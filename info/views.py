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


class AddInfo(View):
    def get(self, request):
        try:
            json_files = [os.path.abspath('datasets/category.json'), os.path.abspath('datasets/location.json'),
                          os.path.abspath('datasets/user.json'), os.path.abspath('datasets/ad.json'), ]

            with open(json_files[0], 'r', encoding='utf-8') as jsonf:
                data = json.loads(jsonf.read())
            for item in data.values():
                cat = Category()
                cat.pk = item["Id"]
                cat.name = item["name"]
                cat.save()

            with open(json_files[1], 'r', encoding='utf-8') as jsonf:
                data = json.loads(jsonf.read())
            for item in data.values():
                location = Location()
                location.pk = item["Id"]
                location.name = item["name"]
                location.lat = item["lat"]
                location.lng = item["lng"]

                location.save()

            with open(json_files[2], 'r', encoding='utf-8') as jsonf:
                data = json.loads(jsonf.read())
            for item in data.values():
                user = User()
                user.pk = item["Id"]
                user.first_name = item["first_name"]
                user.last_name = item.get("last_name")
                user.username = item["username"]
                user.password = item["password"]
                user.role = item["role"]
                user.age = item["age"]

                user.save()
                user.locations.add(item["location_id"])

            with open(json_files[3], 'r', encoding='utf-8') as jsonf:
                data = json.loads(jsonf.read())
            for item in data.values():
                ad = Ad()
                ad.pk = item["Id"]
                ad.name = item["name"]
                ad.author_id = item["author_id"]
                ad.description = item.get("description", None)
                ad.price = int(item["price"])
                ad.is_published = bool(item["is_published"])
                ad.category_id = item.get("category_id", None)

                ad.save()

            return HttpResponse("Данные успешно выгружены", status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
