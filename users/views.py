import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from homework_28 import settings
from users.models import User, Location


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.annotate(total_ads=Count("ad"))
        self.object_list = self.object_list.prefetch_related("locations")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
                "total_ads": user.total_ads,
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        try:
            user = User.objects.create(
                username=user_data["username"],
                password=user_data["password"],
                first_name=user_data["first_name"],
                last_name=user_data.get("last_name", None),
                role=user_data["role"],
                age=user_data["age"],
            )

            for location_name in user_data["locations"]:
                location, _ = Location.objects.get_or_create(name=location_name)
                user.locations.add(location)

            return JsonResponse({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": [location.name for location in user.locations.all()],
            }, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object = self.get_object()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all())),
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data.get("last_name", None)
        self.object.age = user_data["age"]

        for location_name in user_data["locations"]:
            location, _ = Location.objects.get_or_create(name=location_name)
            self.object.locations.add(location)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all())),
        })

@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
