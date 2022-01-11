import re
from accounts.models import settings
from django.urls import reverse
from django.db import models

# Create your models here.
class Post(models.Model): 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='instagramsns/post/%Y/%m/%d')
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.caption

    def extract_tag_list(self):
        tag_name_list = re.findall(r'#([a-zA-Z\dㄱ-힣]+)', self.caption)
        tag_list = []                                           # list 형식
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)   # (object, created) 튜플 형식 반환
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("instagramsns:post_detail", args=[self.pk])

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name