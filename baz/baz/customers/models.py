from django.db import models
import uuid
import datetime


def _hash():
    return uuid.uuid4().hex


# Create your models here.

class Interval(models.Model):
    display_name = models.CharField(max_length=255)
    week_value = models.IntegerField()

    def __str__(self):
        return self.display_name


class Customer(models.Model):
    name = models.CharField(max_length=255, default=None)
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE, default=None)
    signature = models.CharField(max_length=255, db_index=True, default=_hash())
    future_sending = models.DateTimeField(default=datetime.datetime.now)
    schedule_signature = models.CharField(max_length=255, db_index=True, default=_hash())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.signature = self.hash()
        super().save(force_insert, force_update, using, update_fields)

    def hash(self):
        return hash()

    def __str__(self):
        return self.name


class Target(models.Model):
    STATUS = (
        (0, "pending"),
        (1, "completed"),
        (2, "failed"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    status = models.IntegerField(db_index=True, choices=STATUS, default=0)

    def __str__(self):
        return self.email
