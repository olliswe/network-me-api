from faker import Faker
from accounts.models import User, Category
from api.models import Job
from django.utils import timezone
from datetime import timedelta
from random import randint

fake = Faker()


employer_cat = Category.objects.get(id=2)

fake_users = []

## creating 50 employers
for _ in range(50):
    user = User.objects.create_user(email=fake.email(), password="password123")
    user.category = employer_cat
    user.telephone_number = fake.phone_number()
    user.organization = fake.company()
    user.save()
    fake_users.append(user)


for employer in User.objects.filter(category=employer_cat):
    for _ in range(5):
        job = Job.objects.create(
            deadline=timezone.now() + timedelta(days=randint(7, 100)),
            title=fake.job(),
            description=fake.text(max_nb_chars=1000, ext_word_list=None),
            employer=employer,
        )
