from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics
from .models import Job, Application, ApplicationAttachment, Message
from .serializers import (
    JobSerializer,
    ApplicationSerializer,
    JobSeekerJobSerializer,
    EmployerJobSerializer,
    GetApplicationSerializer,
    MessageSerializer,
)
from django.db.models import Count
import boto3
import mimetypes
from django.conf import settings
from django.utils import timezone

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.S3UPLOAD_REGION,
)


class JobViewSet(viewsets.ModelViewSet):  # handles GETs for many Jobs
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class JobSeekerJobSearch(generics.ListAPIView):
    serializer_class = JobSeekerJobSerializer
    queryset = Job.manager.open()
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "employer__organization"]

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        for instance in args[0]:
            user_ids = []
            for application in instance.applications.all():
                user_ids.append(application.author.id)
            if user.id in user_ids:
                instance.applied = True
            else:
                instance.applied = False
        return super(JobSeekerJobSearch, self).get_serializer(*args, **kwargs)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author", "job")


class MessageViewset(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)


@api_view(["GET"])
def get_inbox(request):
    queryset = Message.objects.filter(recipient=request.user)
    serializer = MessageSerializer(queryset, many=True)
    data = serializer.data
    return Response(data)


@api_view(["GET"])
def employer_open_positions(request):
    employer_id = request.user.id
    queryset = Job.manager.open().filter(employer__id=employer_id)
    serializer = EmployerJobSerializer(queryset, many=True)
    data = serializer.data
    return Response(data)


@api_view(["GET"])
def employer_job(request, slug=None):
    employer = request.user
    job = get_object_or_404(Job, slug=slug)
    serializer = EmployerJobSerializer(job, many=False)
    data = serializer.data
    return Response(data)


@api_view(["GET"])
def employer_closed_positions(request):
    employer_id = request.user.id
    queryset = Job.manager.closed().filter(employer__id=employer_id)
    serializer = EmployerJobSerializer(queryset, many=True)
    data = serializer.data
    return Response(data)


@api_view(["GET"])
def employer_get_application(request, slug=None):
    employer_id = request.user.id
    queryset = Application.objects.get(slug=slug)
    serializer = GetApplicationSerializer(queryset, many=False)
    data = serializer.data
    return Response(data)


@api_view(["GET"])
def jobseeker_get_job(request, slug=None):
    job = Job.objects.get(slug=slug)
    user_ids = []
    for application in job.applications.all():
        user_ids.append(application.author.id)
    if request.user.id in user_ids:
        job.applied = True
    else:
        job.applied = False
    serializer = JobSeekerJobSerializer(job, many=False)
    data = serializer.data
    return Response(data)


class MostRecentJobs(generics.ListAPIView):
    serializer_class = JobSeekerJobSerializer
    queryset = Job.manager.open().order_by("-post_date")[:10]

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        for instance in args[0]:
            user_ids = []
            for application in instance.applications.all():
                user_ids.append(application.author.id)
            if user.id in user_ids:
                instance.applied = True
            else:
                instance.applied = False
        return super(MostRecentJobs, self).get_serializer(*args, **kwargs)


class MostPopularJobs(generics.ListAPIView):
    serializer_class = JobSeekerJobSerializer
    queryset = (
        Job.manager.open()
        .annotate(num_applications=Count("applications"))
        .order_by("-num_applications")[:10]
    )

    def get_serializer(self, *args, **kwargs):
        user = self.request.user
        for instance in args[0]:
            user_ids = []
            for application in instance.applications.all():
                user_ids.append(application.author.id)
            if user.id in user_ids:
                instance.applied = True
            else:
                instance.applied = False
        return super(MostPopularJobs, self).get_serializer(*args, **kwargs)


@api_view(["GET"])
def sign_s3_upload(request):
    object_name = request.GET["objectName"]
    key = object_name
    content_type = mimetypes.guess_type(object_name)[0]
    print(content_type)
    # signed_url = s3_client.generate_url(
    #     300,
    #     "PUT",
    #     settings.AWS_STORAGE_BUCKET_NAME,
    #     settings.AWS_FOLDER_NAME + "/" + object_name,
    #     headers={"Content-Type": content_type, "x-amz-acl": "public-read"},
    # )
    signed_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": key,
            "ACL": "public-read",
        },
    )
    get_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": key},
    )
    print(signed_url)
    return Response(
        {
            "signedUrl": signed_url,
            "getUrl": get_url,
            "filename": request.GET["objectName"],
            "key": key,
        }
    )


@api_view(["POST"])
def apply_to_job(request):
    job = Job.objects.get(id=int(request.data["job_id"]))
    application = Application.objects.create(
        cover_letter=request.data["coverLetter"],
        author=request.user,
        job=job,
        date=timezone.now(),
    )
    if request.data["CV"]:
        application.cv = request.data["CV"]["key"]
    application.save()
    for item in request.data["uploads"]:
        upload = item["upload"]
        if upload:
            ApplicationAttachment.objects.create(
                attachment=upload["key"], application=application
            )
    return Response("Success")


@api_view(["GET"])
def get_user_applications(request):
    applications = Application.objects.filter(author=request.user)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)
