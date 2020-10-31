from django.db import models
import datetime


# Create your models here.
class Email(models.Model):
    FAILED = 0
    SUCCESSED = 1
    STATUSES = (
        (FAILED, "failed"),
        (SUCCESSED, "successed"),
    )
    to = models.CharField(max_length=255, db_index=True)
    status = models.IntegerField(db_index=True, choices=STATUSES)
    sent_time = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.pk
