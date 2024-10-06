from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from custom_auth.models import CustomUser
import django.utils.timezone as timezone



class Park(models.Model):
    name = models.CharField(max_length=127)
    description = models.TextField(max_length=511)
    
    # Location
    lat = models.FloatField()
    lng = models.FloatField()
    city = models.CharField(max_length=127)
    district = models.CharField(max_length=127)

    # Impressions
    num_likes = models.IntegerField(default=0, validators=[
            MinValueValidator(0)
        ])
    num_comments = models.IntegerField(default=0, validators=[
            MinValueValidator(0)
        ])
    rating = models.FloatField(default=0, validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ] )

    # Media
    park_image_1 = models.ImageField(upload_to='static/images/park_images')
    park_image_2 = models.ImageField(upload_to='static/images/park_images', null=True, blank=True)
    park_image_3 = models.ImageField(upload_to='static/images/park_images', null=True, blank=True)
    park_video = models.FileField(upload_to='static/videos/park_videos', null=True, blank=True)

    # Availability
    availability = models.BooleanField(default=True)
    work_hours_start = models.TimeField(blank=True, null=True)
    work_hours_end = models.TimeField(blank=True, null=True) 

    def __str__(self):
        return str(self.name)
    
    def location(self):
        return f"{self.city} {self.district}"
        
    class Meta:
        ordering = ['-rating']


class Like(models.Model):

    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    park = models.ForeignKey(Park, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_last_modified = models.DateTimeField(auto_now=True, editable=True)

    is_active = models.BooleanField(default=True)


    def __str__(self) -> str:
        return f"{self.park} liked by {self.author}"
    

class Comment(models.Model):

    content = models.TextField(max_length=255)

    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    park = models.ForeignKey(Park, on_delete=models.SET_NULL, null=True)

    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_last_modified = models.DateTimeField(auto_now=True, editable=True)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.park} commented by {self.author}"
