import re
from accounts.models import settings
from django.urls import reverse
from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# user
# -> Post.objects.filter(author=user)
# -> user.post_set.all()
# related_name은 DB 스키마와는 상관없지만 djangoORM과 상관이 있다.

class Post(BaseModel): 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='instagramsns/post/%Y/%m/%d')
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_post_set')

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

    # 어떤 사용자가 어떤 포스팅에 대해 좋아요를 눌렀는지 확인할 함수
    # like_user_set에 존재하는 user면 True, 아니면 False
    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering =['-id']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']