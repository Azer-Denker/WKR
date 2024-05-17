from .serializers import (PatientRegistrationSerializer,
                          PatientProfileSerializer,
                          PatientHistorySerializer,
                          AppointmentSerializerPatient)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from patient.models import Patient, Appointment, PatientHistory


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Patient').exists())


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='Patient').exists()
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
                    'message': "You are not authorised to login as a Patient"
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
        registration_serializer = PatientRegistrationSerializer(
            data=request.data.get('user_data'))
        profile_serializer = PatientProfileSerializer(
            data=request.data.get('profile_data'))
        checkregistration = registration_serializer.is_valid()
        checkprofile = profile_serializer.is_valid()
        if checkregistration and checkprofile:
            patient = registration_serializer.save()
            profile_serializer.save(user=Patient)
            return Response({
                'user_data': registration_serializer.data,
                'profile_data': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registration_serializer.errors,
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PatientProfileView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        user = request.user
        profile = Patient.objects.filter(user=user).get()
        user_serializer = PatientRegistrationSerializer(user)
        profile_serializer = PatientProfileSerializer(profile)
        return Response({
            'user_data': user_serializer.data,
            'profile_data': profile_serializer.data

        }, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        profile = Patient.objects.filter(user=user).get()
        profile_serializer = PatientProfileSerializer(
            instance=profile, data=request.data.get('profile_data'), partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({
                'profile_data': profile_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                'profile_data': profile_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class PatientHistoryView(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        user = request.user
        user_patient = Patient.objects.filter(user=user).get()
        history = PatientHistory.objects.filter(patient=user_patient)
        history_serializer = PatientHistorySerializer(history, many=True)
        return Response(history_serializer.data, status=status.HTTP_200_OK)


class AppointmentViewPatient(APIView):
    permission_classes = [IsPatient]

    def get(self, request):
        user = request.user
        user_patient = Patient.objects.filter(user=user).get()
        history = PatientHistory.objects.filter(patient=user_patient).latest('admit_date')
        appointment = Appointment.objects.filter(status=True, patient_history=history)
        history_serializer = AppointmentSerializerPatient(appointment, many=True)
        return Response(history_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        user_patient = Patient.objects.filter(user=user).get()
        history = PatientHistory.objects.filter(patient=user_patient).latest('admit_date')
        serializer = AppointmentSerializerPatient(
            data=request.data)
        if serializer.is_valid():
            serializer.save(patient_history=history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
