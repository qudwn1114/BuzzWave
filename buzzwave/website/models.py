from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    membername = models.CharField(default='', max_length=100, verbose_name='회원명')
    phone = models.CharField(default='', max_length=30, verbose_name='전화번호')
    birth = models.DateField(null=True, verbose_name='생년월일')
    company = models.CharField(default='', max_length=50, verbose_name='회사')
    withdrawal_at = models.DateTimeField(null=True, verbose_name='탈퇴일')
    email_verified = models.BooleanField(default=False, verbose_name='이메일 인증여부')

    class Meta:
        db_table='auth_profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Subscriber(models.Model):
    email = models.EmailField(verbose_name='이메일', unique=True)
    is_activate = models.BooleanField(default=True, verbose_name='활성화여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='최초구독일')

    class Meta:
        db_table='subscriber'

class Blog(models.Model):
    image = models.ImageField(null=True, upload_to="image/blog/", verbose_name="썸네일")
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog"

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='태그명', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tag"


class BlogTag(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_tag')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='blog_tag')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "blog_tag"