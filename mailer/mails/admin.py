from django.contrib import admin
from .models import Email


class EmailAdmin(admin.ModelAdmin):
    list_display = ('to', 'status', 'sent_time')
    def has_add_permission(self, request):
        return False


# Register your models here.
admin.site.register(Email, EmailAdmin)
