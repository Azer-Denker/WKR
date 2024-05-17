from django.contrib import admin
from . models import Patient, PatientHistory, Appointment, PatientCost

# admin.site.register(Patient)
# admin.site.register(PatientHistory)
admin.site.register(Appointment)
admin.site.register(PatientCost)


class PatientCost(admin.TabularInline):
    model = PatientCost


class PatientAppointment(admin.TabularInline):
    model = Appointment


class PatientHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'assigned_doctor', 'admit_date', 'department', 'release_date')
    inlines = [PatientAppointment, PatientCost]


admin.site.register(PatientHistory, PatientHistoryAdmin)


class PatientHistoryInline(admin.StackedInline):
    model = PatientHistory
    

class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'address', 'mobile')
    inlines = [PatientHistoryInline]


admin.site.register(Patient, PatientAdmin)
