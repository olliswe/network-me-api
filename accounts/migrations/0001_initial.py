# Generated by Django 2.2.3 on 2019-07-17 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=225, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=225, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=225, null=True, verbose_name='Last Name')),
                ('organization', models.CharField(blank=True, max_length=225, null=True, unique=True, verbose_name='Organization Name')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, default='avatars/placeholder.png', null=True, upload_to='avatars/', verbose_name='Avatar')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Category', verbose_name='User Category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
