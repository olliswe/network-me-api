from django.db import models
from accounts.models import User



class Job(models.Model):
    post_date = models.DateTimeField(verbose_name='Posted on', auto_now_add=True)
    deadline = models.DateTimeField(verbose_name = 'Deadline')
    title = models.TextField(verbose_name="Job Title")
    description = models.TextField(verbose_name="Job Description")
    employer = models.ForeignKey(User, verbose_name="Employer", on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    def has_user_applied(self, user):
        '''

        :param user: a FirebaseUser object
        :return: whether the given user has applied to the form
        '''
        user_ids = []
        for application in self.application_set.all():
            user_ids.append(application.author.id)
        if user.id in user_ids:
            return True
        else:
            return False

    # def get_application(self, user):
    #     return self.application_set.all().filter(author__id = user.id)


class JobAttachment(models.Model):
    attachment = models.FileField(verbose_name="Attachment", upload_to='job_attachment/')
    job = models.ForeignKey(Job, verbose_name="Job", on_delete=models.CASCADE)


class Application(models.Model):
    cv = models.FileField(verbose_name="CV", upload_to='cvs/')
    cover_letter = models.TextField(verbose_name="Cover Letter", null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(Job, verbose_name = "Job", on_delete=models.CASCADE)

class ApplicationAttachment(models.Model):
    attachment = models.FileField(verbose_name='Attachment', upload_to='application_attachments/')
    application = models.ForeignKey(Application, verbose_name="Application", on_delete=models.CASCADE)
