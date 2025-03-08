from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    phone_num = models.CharField(max_length=10, default='None')
    avatar = models.ImageField(upload_to='images/avatars', default='images/avatars/profileAvatar.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"
