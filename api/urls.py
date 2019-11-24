from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "api"


router = routers.DefaultRouter()
router.register(r"job", views.JobViewSet)
router.register(r"application", views.ApplicationViewSet)
router.register(r"messages", views.MessageViewset)


urlpatterns = [
    path("", include(router.urls)),
    # EMPLOYER ROUTES
    path("employer/open", views.employer_open_positions),
    path("employer/closed", views.employer_closed_positions),
    path("employer/get_job/<str:slug>", views.employer_job),
    path("employer/get_application/<str:slug>", views.employer_get_application),
    # JOBSEEKER ROUTES
    path("jobseeker/open_jobs", views.JobSeekerJobSearch.as_view()),
    path("jobseeker/most_recent", views.MostRecentJobs.as_view()),
    path("jobseeker/most_popular", views.MostPopularJobs.as_view()),
    path("jobseeker/get_job/<str:slug>", views.jobseeker_get_job),
    path("jobseeker/post_application", views.apply_to_job),
    path("jobseeker/all_applications", views.get_user_applications),
    # OTHER
    path("s3/sign/", views.sign_s3_upload),
    path("get_messages/", views.get_inbox),
]
