from django.conf.urls import url, include
from rest_framework import routers
from .views import UserViewSet, current_user
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    path('current_user/', current_user),
    url(r'^api-token-refresh/', refresh_jwt_token),

]