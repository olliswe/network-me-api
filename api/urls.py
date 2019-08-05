from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'api'


router = routers.DefaultRouter()
router.register(r'job', views.JobViewSet)
router.register(r'application', views.ApplicationViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('employer/open', views.employer_open_positions),
    path('employer/closed', views.employer_closed_positions ),
    path('employer/get_job/<str:slug>', views.employer_job),
    path('employer/get_application/<str:slug>', views.employer_get_application),
    path('jobseeker/open_jobs', views.JobSeekerJobSearch.as_view())
]