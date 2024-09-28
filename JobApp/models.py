from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    '''
        email = models.EmailField()
        website = models.URLField()
        is_active = models.BooleanField(default=True)
        document = models.FileField(upload_to='documents/')
        profile_picture = models.ImageField(upload_to='images/')
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        STATUS_CHOICES = [
            ('D', 'Draft'),
            ('P', 'Published'),
        ]
        status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    '''
    def __str__(self):
        return self.user.username
    def get_profile_summary(self):
        summary = {
            'Username': self.user.username,
            'Full Name': self.full_name or "Not provided",
            'Phone Number': self.phone_number or "Not provided",
            'Age': self.age if self.age else "Not provided",
            'Bio': self.bio or "Not provided",
            'Address': self.address or "Not provided",
        }
        return summary
    def is_adult(self):
        return self.age >= 18 if self.age else False



class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    domain_name = models.CharField(max_length=255)
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Internship(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    domain_name = models.CharField(max_length=255)
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, null=True, blank=True, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, null=True, blank=True, on_delete=models.CASCADE)
    additional_info = models.TextField()
    applied_date = models.DateField(auto_now_add=True)


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    additional_details = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Applied')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class InternshipApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    additional_details = models.TextField()
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Applied')

    def __str__(self):
        return f"{self.user.username} - {self.internship.title}"
    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)