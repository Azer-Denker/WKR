from .views import (
    CustomAuthToken,
    DoctorAccountViewAdmin,
    DocRegistrationViewAdmin,
    ApproveDoctorViewAdmin,
    AppointmentViewAdmin,
    PatientRegistrationViewAdmin,
    PatientAccountViewAdmin,
    PatientHistoryViewAdmin,
    ApprovePatientViewAdmin,
    ApproveAppointmentViewAdmin,
)

from django.urls import path


urlpatterns = [

    path('login/', CustomAuthToken.as_view(), name='api_admin_login'),

    path('approve/doctors/', ApproveDoctorViewAdmin.as_view(), name='api_doctors_approve_admin'),
    path('approve/doctor/<uuid:pk>/', ApproveDoctorViewAdmin.as_view(), name='api_doctor_detail_approve_admin'),

    path('approve/patients/', ApprovePatientViewAdmin.as_view(), name='api_patients_approve_admin'),
    path('approve/Patient/<uuid:pk>/', ApprovePatientViewAdmin.as_view(), name='api_patient_detail_approve_admin'),

    path('approve/appointments/', ApproveAppointmentViewAdmin.as_view(), name='api_appointment_approve_admin'),
    path('approve/appointment/<int:pk>', ApproveAppointmentViewAdmin.as_view(),
         name='api_appointment_approve_detail_admin'),

    path('doctor/registration/', DocRegistrationViewAdmin.as_view(), name='api_doctors_registration_admin'),
    path('doctors/', DoctorAccountViewAdmin.as_view(), name='api_doctors_admin'),
    path('doctor/<uuid:pk>/', DoctorAccountViewAdmin.as_view(), name='api_doctor_detail_admin'),

    path('Patient/registration/', PatientRegistrationViewAdmin.as_view(), name='api_patient_registration_admin'),
    path('patients/', PatientAccountViewAdmin.as_view(), name='api_patients_admin'),
    path('Patient/<uuid:pk>/', PatientAccountViewAdmin.as_view(), name='api_patient_detail_admin'),
    path('Patient/<uuid:pk>/history/', PatientHistoryViewAdmin.as_view(), name='api_patient_history_admin'),
    path('Patient/<uuid:pk>/history/<int:hid>/', PatientHistoryViewAdmin.as_view(), name='api_patient_history_admin'),

    path('appointments/', AppointmentViewAdmin.as_view(), name='api_appointments_admin'),
    path('appointment/<int:pk>/', AppointmentViewAdmin.as_view(), name='api_appointment_detail_admin'),
]

app_name = 'hospitalAdmin'
