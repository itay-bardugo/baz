from django.db import models
import uuid


# Create your models here.
class Timer(models.Model):
    PENDING = 0
    SETTING_UP = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
    STOPPED = 5

    STATUS = (
        (PENDING, "pending"),
        (SETTING_UP, "setting up..."),
        (RUNNING, "running"),
        (COMPLETED, "completed"),
        (FAILED, "failed"),
        (STOPPED, "stopped"),
    )
    status = models.IntegerField(db_index=True, choices=STATUS)
    signature = models.CharField(max_length=255, db_index=True)
    sleep_time = models.IntegerField(null=True)
    thread_id = models.CharField(max_length=255)
    action_date = models.DateTimeField()
    return_address = models.CharField(max_length=255)
    param = models.TextField(default="", null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.signature = self.make_signature()
        super().save(force_insert, force_update, using, update_fields)

    def make_signature(self):
        return uuid.uuid4().hex

    def __str__(self):
        return str(self.id)