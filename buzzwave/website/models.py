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