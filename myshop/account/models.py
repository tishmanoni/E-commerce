from django.db import models
from django_countries.fields import CountryField

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    country = CountryField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.photo.url))
    image_tag.short_description = 'Image'

    
    

