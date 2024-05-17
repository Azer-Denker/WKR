from .views import RegistrationView, CustomAuthToken, DoctorProfileView, DoctorAppointmentView
from django.urls import path
from .token import CustomTokenObtainPairView, CustomTokenRefreshView


app_name = 'doctor'
urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='api_doctor_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_doctor_login'),
    path('profile/', DoctorProfileView.as_view(), name='api_doctor_profile'),
    path('appointments/', DoctorAppointmentView.as_view(), name='api_doctor_profile'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
