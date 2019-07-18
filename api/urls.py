from django.urls import path, include
from rest_framework import routers
from .views import JobViewSet, ApplicationViewSet

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'job', JobViewSet)
router.register(r'application', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls))
]