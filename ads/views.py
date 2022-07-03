import json
import os

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from ads.models import Ad, Category
from homework_28 import settings
from users.models import User


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                "author": ad.author.first_name,
                "category": ad.category.name,
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "price", "description", "is_published", "author", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, pk=ad_data["author_id"])
        category = get_object_or_404(Category, pk=ad_data["category_id"])
        try:
            ad = Ad.objects.create(
                name=ad_data["name"],
                price=ad_data["price"],
                description=ad_data.get("description", None),
                is_published=ad_data["is_published"],
                author=author,
                category=category
            )

            return JsonResponse({
                "id": ad.id,
                "name": ad.name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                "author": ad.author.first_name,
                "category": ad.category.name,
            }, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "author": self.object.author.first_name,
            "category": self.object.category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "price", "description", "is_published", "author", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]

        self.object.author = get_object_or_404(User, pk=ad_data["author_id"])
        self.object.category = get_object_or_404(Category, pk=ad_data["category_id"])

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "author": self.object.author.first_name,
            "category": self.object.category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "author": self.object.author.first_name,
            "category": self.object.category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class CatListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        response = []
        for cat in self.object_list:
            response.append({
                "id": cat.id,
                "name": cat.name,
            })

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CatCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        try:
            cat = Category.objects.create(
                name=cat_data["name"]
            )

            return JsonResponse({
                "id": cat.id,
                "name": cat.name,
            }, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        cat_data = json.loads(request.body)
        self.object.name = cat_data["name"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
