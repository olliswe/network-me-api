from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, current_user
from django.urls import path
from django.shortcuts import redirect

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


def redirect_to_network_me(request):
    return redirect("https://networkmesl-app.firebaseapp.com/login")


urlpatterns = [
    url(r"", include(router.urls)),
    url(r"^auth/", include("rest_auth.urls")),
    path("current_user/", current_user),
    path("login/", redirect_to_network_me),
    path("services/", include("django.contrib.auth.urls")),
]
