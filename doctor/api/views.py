from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from .serializers import DoctorRegistrationSerializer, DoctorProfileSerializer, DoctorAppointmentSerializer

from doctor.models import Doctor

from patient.models import Appointment


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='doctor').exists())


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='doctor').exists()

        if not user.status:
            return Response(
                {
                    'message': "Your account is not approved by admin yet!"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        elif not account_approval:
            return Response(
                {
                    'message': "You are not authorised to login as a doctor"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    permission_classes = []

    def post(self, request):
        registration_serializer = DoctorRegistrationSerializer(data=request.data.get('user_data'))
        profile_serializer = DoctorProfileSerializer(data=request.data.get('profile_data'))
        check_registration = registration_serializer.is_valid()
        check_profile = profile_serializer.is_valid()
        if check_registration and check_profile:
            doctor = registration_serializer.save()
            profile_serializer.save(user=doctor)
            return Response({
                'user_data': registration_serializer.data,
                'profile_data': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registration_serializer.errors,
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class DoctorProfileView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        user = request.user
        profile = Doctor.objects.filter(user=user).get()
        user_serializer = DoctorRegistrationSerializer(user)
        profile_serializer = DoctorProfileSerializer(profile)
        return Response({
            'user_data': user_serializer.data,
            'profile_data': profile_serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        profile = Doctor.objects.filter(user=user).get()
        profile_serializer = DoctorProfileSerializer(
            instance=profile, data=request.data.get('profile_data'), partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({
                'profile_data': profile_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class DoctorAppointmentView(APIView):
    permission_classes = [IsDoctor]

    def get(self, request):
        user = request.user
        user_doctor = Doctor.objects.filter(user=user).get()
        appointments = Appointment.objects.filter(doctor=user_doctor, status=True).order_by('appointment_date',
                                                                                            'appointment_time')
        appointment_serializer = DoctorAppointmentSerializer(appointments, many=True)
        return Response(appointment_serializer.data, status=status.HTTP_200_OK)
