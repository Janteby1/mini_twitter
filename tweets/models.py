from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone #make sure to set the timezone 

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    '''
    we can add aditional attributes but Included in the django user model are these attributes:
    Username, Password, Email address, firstname, lastname
    '''

    def to_json(self):
        return {
            "email": user.email,
            "username": user.username,
        }

class Tweet(models.Model):
    content = models.CharField(max_length=200)
    link = models.URLField(max_length=120, null = True, default = None)
    tags = models.CharField(max_length=120, null = True, default = None)

    created_at = models.DateTimeField(editable=False)
    likes = models.IntegerField(default=0)

    user = models.ForeignKey(User, related_name ="author")
    repost = models.ManyToManyField(User)

    # this is a custom save method
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        super(Tweet, self).save(*args, **kwargs)

    # this create a dictionary from an object to use with ajax
    def to_json(self):
        return {
            "id": self.id,
            "link": self.link,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at, 
            "likes": self.likes,
            "user": self.user.username,
            "repost": self.user.id
        }



