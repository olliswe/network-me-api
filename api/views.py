from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
#from rest_framework import permissions
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer, JobSeekerJobSerializer, EmployerJobSerializer,\
                        GetApplicationSerializer


class JobViewSet(viewsets.ModelViewSet):  # handles GETs for many Jobs
    serializer_class = JobSerializer
    queryset = Job.objects.all()

    # def retrieve(self, request, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data
    #     if request.user.category.name == 'Job Seeker':
    #         instance.applied = instance.has_user_applied(request.user)
    #         serializer = JobUserSerializer
    #         data = serializer.data
    #     else:
    #         serializer = self.get_serializer(instance)
    #         data = serializer.data
    #     return Response(data)

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return super(CustomSearchFilter, self).get_search_fields(view, request)



class JobSeekerJobSearch(generics.ListAPIView):
    serializer_class = JobSeekerJobSerializer
    queryset = Job.manager.open()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'employer__organization']

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

    # def get_queryset(self):
    #     queryset = Job.manager.open()
    #     user = self.request.user
    #     for instance in queryset:
    #         user_ids = []
    #         for application in instance.applications.all():
    #             user_ids.append(application.author.id)
    #         if user.id in user_ids:
    #             instance.applied = True
    #         else:
    #             instance.applied = False
    #     return queryset









class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('author','job',)



@api_view(['GET'])
def employer_open_positions(request):
    employer_id = request.user.id
    queryset = Job.manager.open().filter(employer__id = employer_id)
    serializer = EmployerJobSerializer(queryset, many=True)
    data = serializer.data
    return Response(data)

@api_view(['GET'])
def employer_job(request, slug=None):
    employer = request.user
    job = get_object_or_404(Job, slug=slug)
    serializer = EmployerJobSerializer(job, many=False)
    data = serializer.data
    return Response(data)



@api_view(['GET'])
def employer_closed_positions(request):
    employer_id = request.user.id
    queryset = Job.manager.closed().filter(employer__id = employer_id)
    serializer = EmployerJobSerializer(queryset, many=True)
    data = serializer.data
    return Response(data)

@api_view(['GET'])
def employer_get_application(request, slug=None):
    employer_id = request.user.id
    queryset = Application.objects.get(slug=slug)
    serializer = GetApplicationSerializer(queryset, many=False)
    data = serializer.data
    return Response(data)



# class JobSeekerJobSearchView(HaystackViewSet):
#     index_models = [Job]
#     serializer_class = JobSeekerJobSearchSerializer

