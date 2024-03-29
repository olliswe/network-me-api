# Generated by Django 2.2.3 on 2019-07-31 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import randomslugfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='cvs/', verbose_name='CV')),
                ('cover_letter', models.TextField(blank=True, null=True, verbose_name='Cover Letter')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('slug', randomslugfield.fields.RandomSlugField(blank=True, editable=False, length=7, max_length=7, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(auto_now_add=True, verbose_name='Posted on')),
                ('deadline', models.DateTimeField(verbose_name='Deadline')),
                ('title', models.TextField(verbose_name='Job Title')),
                ('description', models.TextField(verbose_name='Job Description')),
                ('slug', randomslugfield.fields.RandomSlugField(blank=True, editable=False, length=7, max_length=7, unique=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Employer')),
            ],
        ),
        migrations.CreateModel(
            name='JobAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='job_attachment/', verbose_name='Attachment')),
                ('slug', randomslugfield.fields.RandomSlugField(blank=True, editable=False, length=7, max_length=7, unique=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Job', verbose_name='Job')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to='application_attachments/', verbose_name='Attachment')),
                ('slug', randomslugfield.fields.RandomSlugField(blank=True, editable=False, length=7, max_length=7, unique=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Application', verbose_name='Application')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='api.Job', verbose_name='Job'),
        ),
    ]
