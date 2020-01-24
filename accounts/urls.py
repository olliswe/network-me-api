from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, current_user
from django.urls import path

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    url(r"", include(router.urls)),
    url(r"^auth/", include("rest_auth.urls")),
    path("current_user/", current_user),
    path("services/", include("django.contrib.auth.urls")),
]
