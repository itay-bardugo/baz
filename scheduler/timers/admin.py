from django.contrib import admin
from .models import Timer


class TimerAdmin(admin.ModelAdmin):
    readonly_fields = ("action_date", 'thread_id', 'sleep_time', 'signature', 'status', "param", "return_address")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Timer, TimerAdmin)
