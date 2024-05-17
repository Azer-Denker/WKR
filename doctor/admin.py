from django.contrib import admin
from . models import Doctor
from patient.models import Appointment


class DoctorAppointment(admin.TabularInline):
    model = Appointment


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'department', 'address', 'mobile', 'user']
    inlines = [DoctorAppointment]


admin.site.register(Doctor, DoctorAdmin)
