import requests
import datetime
from .service.schedule import ScheduleService
from django.contrib import admin
from .repository.customer import CustomerRepository
from django.conf.urls import url
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect

# Register your models here.
from .models import Customer, Target, Interval
import os


class TargetInline(admin.TabularInline):
    model = Target
    readonly_fields = ('status',)
    ordering = ("-status",)


class TargetAdmin(admin.ModelAdmin):
    readonly_fields = ("status",)


class CustomerAdmin(admin.ModelAdmin):
    # change_form_template = 'admin/customer/custom_change_form.html'
    inlines = [
        TargetInline
    ]
    list_display = (
        'id',
        'name',
        'interval',
        'customer_actions'
    )
    readonly_fields = (
        "signature",
        "schedule_signature"
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<customer_id>.+)/schedule/$',
                self.admin_site.admin_view(self.schedule),
                name='customer-schedule',
            ),
            url(
                r'^(?P<schedule_signature>.+)/schedule/stop/$',
                self.admin_site.admin_view(self.stop_schedule),
                name='customer-stop-schedule',
            )
        ]
        return custom_urls + urls

    def stop_schedule(self, request, schedule_signature):
        ScheduleService().stop(schedule_signature)
        self.message_user(request, "schedule has stopped")
        return HttpResponseRedirect("../..")

    def schedule(self, request, customer_id):
        customer = CustomerRepository.find_by_id(customer_id)
        schedule_service = ScheduleService()
        if customer.schedule_signature:
            self.message_user(request, 'schedule process already exists. please stop it first.')
            return HttpResponseRedirect("../..")

        if datetime.datetime.now() >= customer.future_sending.replace(tzinfo=None):
            schedule_service.send_mails(customer.id)
        msg = 'failed. try again.'
        if (schedule_signature := ScheduleService().schedule(customer)):
            msg = f"schedule signature is: {schedule_signature}"
        self.message_user(request, msg)
        return HttpResponseRedirect("../..")

    def customer_actions(self, obj):
        if obj.schedule_signature:
            return format_html(
                '<a class="button" href="{}">Schedule</a>&nbsp;'
                '<a class="button" href="{}">Stop</a>',
                reverse('admin:customer-schedule', args=[obj.pk]),
                reverse('admin:customer-stop-schedule', args=[obj.schedule_signature]),
            )
        return format_html(
            '<a class="button" href="{}">Schedule</a>',
            reverse('admin:customer-schedule', args=[obj.pk]),
        )



admin.site.register(Customer, CustomerAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(Interval)
