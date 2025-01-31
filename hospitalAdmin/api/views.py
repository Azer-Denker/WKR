from django.http import Http404
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

from patient.models import (PatientHistory, Appointment)

from account.models import User

from . serializers import (DoctorAccountSerializerAdmin,
                           DoctorRegistrationSerializerAdmin,
                           DoctorRegistrationProfileSerializerAdmin,
                           AppointmentSerializerAdmin,
                           PatientRegistrationSerializerAdmin,
                           PatientRegistrationProfileSerializerAdmin,
                           PatientAccountSerializerAdmin,
                           PatientHistorySerializerAdmin)

from doctor.models import Doctor


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='admin').exists())


class CustomAuthToken(ObtainAuthToken):
    @swagger_auto_schema(operation_summary="Emil adm")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='admin').exists()
        if not account_approval:
            return Response({'message': "You are not authorised to login as an admin"},
                            status=status.HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class DocRegistrationViewAdmin(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(operation_summary="Emil got")
    def post(self, request):
        registration_serializer = DoctorRegistrationSerializerAdmin(
            data=request.data.get('user_data'))
        profile_serializer = DoctorRegistrationProfileSerializerAdmin(
            data=request.data.get('profile_data'))
        checkregistration = registration_serializer.is_valid()
        checkprofile = profile_serializer.is_valid()
        if checkregistration and checkprofile:
            doctor = registration_serializer.save()
            profile_serializer.save(user=Doctor)
            return Response({'user_data': registration_serializer.data, 'profile_data': profile_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'user_data': registration_serializer.errors, 'profile_data': profile_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class DoctorAccountViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_summary="Emil doc acc")
    def get(self, request, pk=None):

        if pk:
            doctor_detail = self.get_object(pk)
            serializer = DoctorAccountSerializerAdmin(doctor_detail)
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        all_doctor = User.objects.filter(groups=1, status=True)
        serializer = DoctorAccountSerializerAdmin(all_doctor, many=True)
        return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Emil pidor2")
    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = DoctorAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('doctors'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        return Response({'doctors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)}, status=status.HTTP_204_NO_CONTENT)


class ApproveDoctorViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):

        if pk:
            doctor_detail = self.get_object(pk)
            serializer = DoctorAccountSerializerAdmin(doctor_detail)
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        all_doctor = User.objects.filter(groups=1, status=False)
        serializer = DoctorAccountSerializerAdmin(all_doctor, many=True)
        return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = DoctorAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('doctors'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'doctors': serializer.data}, status=status.HTTP_200_OK)
        return Response({'doctors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "Doctor approval request with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class ApprovePatientViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):

        if pk:
            doctor_detail = self.get_object(pk)
            serializer = PatientAccountSerializerAdmin(doctor_detail)
            return Response({'patients': serializer.data}, status=status.HTTP_200_OK)
        all_patient = User.objects.filter(groups=2, status=False)
        serializer = PatientAccountSerializerAdmin(all_patient, many=True)
        return Response({'patients': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = PatientAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('patients'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'patients': serializer.data}, status=status.HTTP_200_OK)
        return Response({'patients': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "Patient approval request with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class AppointmentViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):

        if pk:
            appointment_detail = self.get_object(pk)
            serializer = AppointmentSerializerAdmin(appointment_detail)
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        all_appointment = Appointment.objects.filter(status=True)
        serializer = AppointmentSerializerAdmin(all_appointment, many=True)
        return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AppointmentSerializerAdmin(
            data=request.data.get('appointments'))
        if serializer.is_valid():
            serializer.save()
            return Response({
                'appointments': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'appointments': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        saved_appointment= self.get_object(pk)
        serializer = AppointmentSerializerAdmin(
            instance=saved_appointment, data=request.data.get('appointments'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        return Response({'appointments': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_appointment = self.get_object(pk)
        saved_appointment.delete()
        return Response({"message": "Appointment with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class ApproveAppointmentViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    
    def get(self, request, pk=None):

        if pk:
            appointment_detail = self.get_object(pk)
            serializer = AppointmentSerializerAdmin(appointment_detail)
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        all_appointment = Appointment.objects.filter(status=False)
        serializer = AppointmentSerializerAdmin(all_appointment, many=True)
        return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
            saved_appointment= self.get_object(pk)
            serializer = AppointmentSerializerAdmin(
                instance=saved_appointment, data=request.data.get('appointments'), partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
            return Response({'appointments': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_appointment = self.get_object(pk)
        saved_appointment.delete()
        return Response({"message": "Appointment with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class PatientRegistrationViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        registration_serializer = PatientRegistrationSerializerAdmin(
            data=request.data.get('user_data'))
        profile_serializer = PatientRegistrationProfileSerializerAdmin(
            data=request.data.get('profile_data'))
        checkregistration = registration_serializer.is_valid()
        checkprofile = profile_serializer.is_valid()
        if checkregistration and checkprofile:
            patient = registration_serializer.save()
            profile_serializer.save(user=patient)
            return Response({'user_data': registration_serializer.data, 'profile_data': profile_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'user_data': registration_serializer.errors, 'profile_data': profile_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)


class PatientAccountViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            patient_detail = self.get_object(pk)
            serializer = PatientAccountSerializerAdmin(patient_detail)
            return Response({'patients': serializer.data}, status=status.HTTP_200_OK)
        all_patient = User.objects.filter(groups=2, status=True)
        serializer = PatientAccountSerializerAdmin(all_patient, many=True)
        return Response({'patients': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = PatientAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('patients'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'patients': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'patients': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class PatientHistoryViewAdmin(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, pk, hid=None):
        user_patient = get_object_or_404(User, pk=pk).patient
        if hid:
            try:
                history = PatientHistory.objects.get(id=hid)
            except PatientHistory.DoesNotExist:
                raise Http404
            if history.Patient == user_patient:
                serializer = PatientHistorySerializerAdmin(history)
                return Response({'patient_history': serializer.data}, status=status.HTTP_200_OK)
            return Response({"message: This history id `{}` does not belong to the user".format(hid)},
                            status=status.HTTP_404_NOT_FOUND)
        patient_historys = user_patient.patienthistory_set.all()
        serializer = PatientHistorySerializerAdmin(patient_historys, many=True)
        return Response({'patient_history': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk, hid):
        user_patient = get_object_or_404(User, pk=pk).patient
        try:
            history = PatientHistory.objects.get(id=hid)
        except PatientHistory.DoesNotExist:
            raise Http404
        if history.Patient == user_patient:
            serializer = PatientHistorySerializerAdmin(instance=history, data=request.data.get('patient_history'),
                                                       partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'patient_history': serializer.data}, status=status.HTTP_200_OK)
            return Response({'patient_history': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message: This history id `{}` does not belong to the user".format(hid)},
                        status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, hid):
        user_patient = get_object_or_404(User, pk=pk).patient
        try:
            history = PatientHistory.objects.get(id=hid)
        except PatientHistory.DoesNotExist:
            raise Http404
        if history.Patient == user_patient:
            history.delete()
            return Response({"message": "History with id `{}` has been deleted.".format(hid)},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"message: This history id `{}` does not belong to the user".format(hid)},
                        status=status.HTTP_404_NOT_FOUND)
