from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from localflavor.us.models import USStateField, USZipCodeField


# try to refer to settings.AUTH_USER_MODEL instead of referring directly
# to this custom user model
class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=150, unique=True, null=False)
    bio = models.TextField(max_length=1000, blank=True)
    city = models.CharField(max_length=30, blank=True)
    zipcode = USZipCodeField(null=True, blank=True)
    state = USStateField(null=True, blank=True)
    country = models.CharField(max_length=30, blank=True, default="United States")
    birth_date = models.DateField(null=True, blank=True)
    organization = models.CharField(max_length=30, blank=True)
    passcode = models.CharField(max_length=15, blank=True)
    mentor = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_images', blank=True)
    tags = TaggableManager(blank=True, verbose_name='Skills & Interests')


    class Meta(object):
        unique_together = ('email',)


    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('account:index', kwargs={'pk': self.pk})

    def tag_string(self):
        tags = self.tags.all()
        tags_list = []
        for tag in tags:
            tags_list.append(tag.name)

        return ', '.join(tags_list)
