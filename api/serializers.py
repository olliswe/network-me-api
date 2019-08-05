from rest_framework.serializers import ModelSerializer, StringRelatedField, \
    PrimaryKeyRelatedField, BooleanField, ReadOnlyField, Field, FilePathField, SerializerMethodField

from .models import Job, Application
from accounts.serializers import UserSerializer
# from .search_indexes import JobIndex






class JobSerializer(ModelSerializer):
    applications = PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Job
        fields = (
        'id','post_date', 'deadline', 'title', 'description', 'manually_closed', 'employer', 'applications'
        )




class EmployerJobSerializer(ModelSerializer):
    post_date = ReadOnlyField(source="get_timesince_post")
    timed_out = ReadOnlyField(source='is_timed_out')
    deadline = ReadOnlyField(source="format_deadline")
    applications = PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Job
        fields = (
        'id','post_date', 'deadline', 'title', 'description', 'employer', 'applications', 'slug','timed_out',
        'manually_closed'
        )



class JobSeekerJobSerializer(ModelSerializer):
    applied = BooleanField()
    employer = UserSerializer()
    class Meta:
        model = Job
        fields = (
        'id','post_date', 'deadline', 'title', 'description', 'employer','applied'
        )




# class JobSeekerJobSearchSerializer(HaystackSerializerMixin, JobSeekerJobSerializer):
#     class Meta(JobSeekerJobSerializer.Meta):
# #         search_fields = ("text", "title" )
#
# class JobSeekerJobSearchSerializer(HaystackSerializer):
#     class Meta:
#       index_classes = [JobIndex]
#       fields = [
#          'text', 'title', 'organization'
#       ]


class ApplicationSerializer(ModelSerializer):
    employer_id = ReadOnlyField(source='get_employer_id')
    date = ReadOnlyField(source="get_timesince_applied")
    author = UserSerializer()
    class Meta:
        model = Application
        fields = ('id','cv', 'cover_letter', 'author', 'date','job', 'employer_status','slug', 'employer_id')


class GetApplicationSerializer(ModelSerializer):
    employer_id = ReadOnlyField(source='get_employer_id')
    date = ReadOnlyField(source="get_timesince_applied")
    job = EmployerJobSerializer()
    author = UserSerializer()
    class Meta:
        model = Application
        fields = ('id','cv', 'cover_letter', 'author', 'date','job', 'employer_status','slug', 'employer_id')

