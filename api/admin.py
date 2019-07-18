from django.contrib import admin
from .models import Job, JobAttachment, Application, ApplicationAttachment

# Register your models here.


admin.site.register(Job)
admin.site.register(JobAttachment)
admin.site.register(Application)
admin.site.register(ApplicationAttachment)
