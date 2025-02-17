# from django.core.management.base import BaseCommand
# from faker import Faker
# from webapp.models import School, Profile
# from django.contrib.auth.models import User
#
# class Command(BaseCommand):
#     help = 'Generates fake data for testing purposes'
#
#     def handle(self, *args, **kwargs):
#         fake = Faker()
#
#         # Generate fake schools
#         for _ in range(10):  # Generate 10 schools
#             school_name = fake.company()
#             school_slug = fake.slug()
#             school_image = fake.image_url()
#             school_address = fake.address()
#
#             school = School.objects.create(
#                 name=school_name,
#                 slug=school_slug,
#                 image=school_image,
#                 address=school_address
#             )
#
#             # Generate fake users and profiles for each school
#             for _ in range(5):  # Generate 5 users per school
#                 username = fake.user_name()
#                 email = fake.email()
#                 password = fake.password()
#                 user = User.objects.create_user(
#                     username=username,
#                     email=email,
#                     password=password
#                 )
#                 Profile.objects.create(
#                     user=user,
#                     school=school,
#                     mobile_number=fake.phone_number()
#                 )
#
#             self.stdout.write(self.style.SUCCESS(f'Successfully generated fake data for school: {school_name}'))
