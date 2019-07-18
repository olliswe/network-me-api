from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import permissions
from rest_framework.decorators import action

from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer, JobUserSerializer

class JobViewSet(viewsets.ModelViewSet):  # handles GETs for many Jobs
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('employer',)

    def retrieve(self, request, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if request.user.category.name == 'Applicant':
            instance.applied = instance.has_user_applied(request.user)
            serializer = JobUserSerializer
            data = serializer.data
        else:
            serializer = self.get_serializer(instance)
            data = serializer.data
        return Response(data)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        print(data)
        return Response(data)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('author',)

