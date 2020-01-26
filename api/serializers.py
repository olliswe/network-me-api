from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    PrimaryKeyRelatedField,
    BooleanField,
    ReadOnlyField,
    RelatedField,
    Field,
    FilePathField,
    SerializerMethodField,
)

from .models import Job, Application, ApplicationAttachment, Message
from accounts.serializers import UserSerializer

# from .search_indexes import JobIndex


class ApplicationAttachmentSerializer(ModelSerializer):
    class Meta:
        model = ApplicationAttachment
        fields = "__all__"


class SimpleJobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "title", "slug")


class JobSerializer(ModelSerializer):
    applications = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "post_date",
            "deadline",
            "title",
            "description",
            "manually_closed",
            "employer",
            "applications",
            "slug",
        )


class ApplicationJobSerializer(ModelSerializer):
    employer = UserSerializer()
    deadline = ReadOnlyField(source="format_deadline")
    closed = ReadOnlyField(source="is_closed")

    class Meta:
        model = Job
        fields = (
            "id",
            "post_date",
            "deadline",
            "title",
            "description",
            "employer",
            "slug",
            "closed",
        )


class EmployerJobSerializer(ModelSerializer):
    post_date = ReadOnlyField(source="get_timesince_post")
    timed_out = ReadOnlyField(source="is_timed_out")
    formatted_deadline = ReadOnlyField(source="format_deadline")
    applications = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "post_date",
            "deadline",
            "title",
            "description",
            "employer",
            "applications",
            "slug",
            "timed_out",
            "manually_closed",
            "formatted_deadline",
        )


class JobSeekerJobSerializer(ModelSerializer):
    applied = BooleanField()
    employer = UserSerializer()
    timesince_post = ReadOnlyField(source="get_timesince_post")
    deadline = ReadOnlyField(source="format_deadline")
    timeuntil_deadline = ReadOnlyField(source="get_time_until_deadline")
    closed = ReadOnlyField(source="is_closed")

    class Meta:

        model = Job
        fields = (
            "id",
            "post_date",
            "deadline",
            "title",
            "description",
            "employer",
            "applied",
            "timesince_post",
            "timeuntil_deadline",
            "slug",
            "closed",
        )


class ApplicationSerializer(ModelSerializer):
    employer_id = ReadOnlyField(source="get_employer_id")
    author = UserSerializer()
    job = ApplicationJobSerializer()
    date = ReadOnlyField(source="format_date")
    timesince_applied = ReadOnlyField(source="get_timesince_applied")

    class Meta:
        model = Application
        fields = (
            "id",
            "cv",
            "cover_letter",
            "author",
            "date",
            "job",
            "employer_status",
            "slug",
            "employer_id",
            "timesince_applied",
        )


class GetApplicationSerializer(ModelSerializer):
    employer_id = ReadOnlyField(source="get_employer_id")
    date = ReadOnlyField(source="get_timesince_applied")
    job = EmployerJobSerializer()
    author = UserSerializer()
    application_attachments = ApplicationAttachmentSerializer(many=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "cv",
            "cover_letter",
            "author",
            "date",
            "job",
            "employer_status",
            "slug",
            "employer_id",
            "application_attachments",
        )


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ViewMessageSerializer(ModelSerializer):
    author = UserSerializer()
    recipient = UserSerializer()
    job = SimpleJobSerializer()
    formatted_date = ReadOnlyField(source="getFormattedDate")
    days = ReadOnlyField(source="getDaysAgo")

    class Meta:
        model = Message
        fields = [field.name for field in model._meta.fields]
        fields.append("formatted_date")
        fields.append("days")
