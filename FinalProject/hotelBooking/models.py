from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    reservation_type = models.TextField(blank=False, null=False)
    reservation_room = models.TextField(blank=False, null=False)
    reservation_amount = models.IntegerField(blank=False, null=False)
    reservation_dateTime = models.DateTimeField(blank=False, null=False)
    reservation_duration=models.IntegerField(blank=False, null=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_location=models.CharField(blank=False, null=False,max_length=400)
    reservation_id = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        if not self.reservation_id:
            latest_reservation = Reservation.objects.order_by('-reservation_id').first()
            if latest_reservation:
                last_id = int(latest_reservation.reservation_id.split('-')[1])
                new_id = f'R-{last_id + 1:03d}' 
            else:
                new_id = 'R-001'
            
            self.reservation_id = new_id

        super().save(*args, **kwargs)
