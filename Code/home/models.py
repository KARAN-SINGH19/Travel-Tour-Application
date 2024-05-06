from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Member(models.Model):
    memberID = models.CharField(
        blank=False, null=False, max_length=200, unique=True)
    amount = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.memberID:
            latest_Member = Member.objects.order_by('-memberID').first()
            if latest_Member:
                last_id = int(latest_Member.memberID.split('-')[1])
                new_id = f'M-{last_id + 1:03d}'
            else:
                new_id = 'M-001'

            self.memberID = new_id

        super().save(*args, **kwargs)


class offers(models.Model):
    couponCode = models.CharField(max_length=100, blank=False, null=False)
    discountPercentage = models.IntegerField()
    validFor = models.CharField(max_length=200, blank=False, null=False)


class feedback(models.Model):
    feedback = models.TextField(blank=False, null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
