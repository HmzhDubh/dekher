from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Fund(models.Model):

    class Status(models.TextChoices):
        NEW = "new", "New"
        FINISHED = "finished", "Finished"
        IN_PROGRESS = "inProgress", "In Progress"
        PREPARING = "preparing", "Preparing"
        CANCELED = "canceled", "Canceled"

    name = models.CharField(max_length=50)
    description = models.TextField()
    monthly_stock = models.SmallIntegerField(default=1000)
    logo = models.ImageField(upload_to='images/logos', default='images/logos/fundLogo.jpg')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fund_owner')
    members = models.ManyToManyField(User, related_name='fund_members', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now, null=True)
    status = models.CharField(default=Status.NEW, choices=Status.choices, max_length=11)


class Favorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):

    class Rates(models.IntegerChoices):

        STAR1 = 1, 'One Star'
        STAR2 = 2, 'Two Stars'
        STAR3 = 3, 'Three Stars'
        STAR4 = 4, 'Four Stars'
        STAR5 = 5, 'Five Stars'

    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(choices=Rates.choices)
    comment = models.TextField()
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} on {self.fund.fund_name}"