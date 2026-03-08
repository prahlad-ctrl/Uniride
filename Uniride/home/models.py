from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=150)
    branch_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    year = models.IntegerField(null=True)
    sem = models.IntegerField(null=True)
    phone_number = models.IntegerField(null=True)
    personal_address = models.CharField(max_length=255)

    class Meta:
        db_table = "home_account"


class Vehicle(models.Model):
    account_id = models.OneToOneField(Account, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=100)
    vehicle_number = models.IntegerField(null=True)

    class Meta:
        db_table = "home_vehicle"


class PublishRide(models.Model):
    rider_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=False)
    time = models.TimeField(auto_now=False)
    to_where = models.CharField(max_length=150)
    from_where = models.CharField(max_length=150)

    def __str__(self):
        return (
            f"{self.rider_account.user.username}: "
            f"{self.from_where} -> {self.to_where} ({self.date} {self.time})"
        )

    class Meta:
        db_table = "home_publish_ride"


# Backward-compatible aliases for existing imports/usages.
account = Account
vehicle = Vehicle
publish_ride = PublishRide
