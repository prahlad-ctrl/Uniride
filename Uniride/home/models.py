from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    college_name=models.CharField(max_length=150)
    branch_name=models.CharField(max_length=100)
    student_id=models.CharField(max_length=50)
    year=models.IntegerField(null=True)
    sem=models.IntegerField(null=True)
    phone_number=models.IntegerField(null=True)
    personal_address=models.CharField(max_length=255)
class vehicle(models.Model):
    account_id=models.OneToOneField(account,on_delete=models.CASCADE,null=True)
    vehicle_model=models.CharField(max_length=100)
    vehicle_number=models.IntegerField(null=True)
    #vehicle_insurance=
    #vehicle_registeration_city=
    #vehicle_owner_name=
class publish_ride(models.Model):
    vehicle_rider=models.ForeignKey(account,on_delete=models.CASCADE,null=True)
    date=models.DateField(auto_now=False)
    time=models.TimeField(auto_now=False)
    to_where=models.CharField(max_length=150)
    from_where=models.CharField(max_length=150)

    def __str__(self):
        return f"{self.vehicle_rider.user.username}: {self.from_where} -> {self.to_where} ({self.date} {self.time})"



# Readable aliases (non-breaking, no migration needed right now).
Account = account
Vehicle = vehicle
PublishRide = publish_ride
