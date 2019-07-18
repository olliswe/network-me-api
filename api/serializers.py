from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField, BooleanField

from .models import Job, Application
from accounts.serializers import UserSerializer




class JobSerializer(ModelSerializer):
    employer = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Job
        fields = (
        'id','post_date', 'deadline', 'title', 'description', 'employer'
        )

class JobUserSerializer (ModelSerializer):
    applied = BooleanField()
    class Meta:
        model = Job
        fields = (
        'id','post_date', 'deadline', 'title', 'description', 'employer', 'applied'
        )


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ('cv', 'cover_letter', 'author', 'date','job')