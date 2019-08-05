from django.db import models
from accounts.models import User
from django.utils import timezone, timesince
from randomslugfield import RandomSlugField
from django.db.models import Q


class JobManager(models.Manager):
    def open(self):
        return self.filter(deadline__gt=timezone.now(), manually_closed=False)

    def closed(self):
        return self.filter(Q(deadline__lt=timezone.now()) | Q(manually_closed=True))


class Job(models.Model):
    post_date = models.DateTimeField(verbose_name='Posted on', auto_now_add=True)
    deadline = models.DateTimeField(verbose_name = 'Deadline')
    title = models.TextField(verbose_name="Job Title")
    description = models.TextField(verbose_name="Job Description")
    employer = models.ForeignKey(User, verbose_name="Employer", on_delete=models.CASCADE)
    slug = RandomSlugField(length=7)
    manually_closed = models.BooleanField(verbose_name='Manually Closed', default=False)

    objects = models.Manager()
    manager = JobManager()





    def __str__(self):
        return self.title

    @property
    def has_user_applied(self, user):
        '''

        :param user: a User object
        :return: whether the given user has applied to the form
        '''
        user_ids = []
        for application in self.applications.all():
            user_ids.append(application.author.id)
        if user.id in user_ids:
            return True
        else:
            return False


    def get_timesince_post(self):
        return timesince.timesince(self.post_date)


    def format_deadline(self):
        return self.deadline.strftime('%d %B %Y, %H:%M %p')


    @property
    def is_timed_out(self):
        if self.deadline < timezone.now():
            return True
        else:
            return False




class JobAttachment(models.Model):
    attachment = models.FileField(verbose_name="Attachment", upload_to='job_attachment/')
    job = models.ForeignKey(Job, verbose_name="Job", on_delete=models.CASCADE)
    slug = RandomSlugField(length=7)



class Application(models.Model):
    EMPLOYER_STATUS_CHOICES = [('applied','applied'),
                               ('interview','interview'),
                               ('rejected', 'rejected')]
    cv = models.FileField(verbose_name="CV", upload_to='cvs/')
    cover_letter = models.TextField(verbose_name="Cover Letter", null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, verbose_name = "Job", on_delete=models.CASCADE, related_name='applications')
    employer_status = models.CharField(max_length=20, verbose_name="Application Status (for employer)", default='applied',
                                       choices=EMPLOYER_STATUS_CHOICES
                                       )
    slug = RandomSlugField(length=7)

    def get_timesince_applied(self):
        return timesince.timesince(self.date)

    def get_employer_id(self):
        return self.job.employer.id



class ApplicationAttachment(models.Model):
    attachment = models.FileField(verbose_name='Attachment', upload_to='application_attachments/')
    application = models.ForeignKey(Application, verbose_name="Application", on_delete=models.CASCADE)
    slug = RandomSlugField(length=7)


