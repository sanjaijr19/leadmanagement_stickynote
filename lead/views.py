# from datetime import timezone
from django.core.files.base import ContentFile
from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from rest_framework.views import APIView
from policies.utils import sendSignal_record_created, sendSignal_record_updated
# from .models import Lead, LeadSource, LeadNotes

from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework.settings import api_settings
from tenant.utils import tenant_from_request_alluser
from . import models as lead_models
from . import serializers as lead_serializers
from rest_framework import viewsets, generics, status
from lead import signals
from rest_framework.exceptions import NotFound
from .utils import sendSignal_created_record, sendSignal_updated_record, sendSignal_delete_record


# Create your views here.
# lead view class

class LeadBulkCreate(viewsets.ModelViewSet):
    queryset = lead_models.Lead.objects.all()
    serializer_class = lead_serializers.Leadserializer1

    def create(self, request, *args, **kwargs):

        for _ in range(500):
            lead_models.Lead.objects.create(lead_name="Lead Test", designation="Insurance Agent",user_id='94280e54-e3e8-4ebd-82d7-357e1f40fb76',phone_number=1234567891,
                                            email_id="test@testmail.com",address="chennai",lead_status="Converted",lead_score="75%")

        return super().create(request, *args, **kwargs)
class LeadRetrieveView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.Lead.objects.all()
    serializer_class = lead_serializers.LeadSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            x = lead_models.Lead.objects.filter(user=tenant).order_by('-id')
            if x.exists():
                return x
            else:
                raise NotFound({"alert": "Lead Not Found"})

        else:
            return []


# lead create class
class LeadCreateView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.Lead.objects.all()
    serializer_class = lead_serializers.LeadSerializer
    lookup_field = 'id'

    #
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            lead = lead_models.Lead.objects.filter(user=tenant)
            if lead.exists():
                return lead
            else:
                raise NotFound({"alert": "Lead Not Found"})

        else:
            return []

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        serializer = self.get_serializer(data=request.data, context={'user_id': user_id})
        if serializer.is_valid(raise_exception=True):
            leadsource = request.data.get('leadsource', '')
            if leadsource:
                if lead_models.LeadSource.objects.filter(user_id=user_id, lead_source=leadsource).exists():
                    self.perform_create(serializer, user_id)
                    model = lead_models.Lead
                    headers = self.get_success_headers(serializer.data)
                    sendSignal_created_record(serializer, user_id, model)
                    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
                else:
                    return Response({'error': 'Creating lead choice Fail...!!!'})
            else:
                self.perform_create(serializer, user_id)
                model = lead_models.Lead
                headers = self.get_success_headers(serializer.data)
                sendSignal_created_record(serializer, user_id, model)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            return Response({'error': 'Creating lead Failed...!!!'})

    def perform_create(self, serializer, user_id):
        serializer.save(user_id=user_id)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            if lead_models.LeadSource.objects.filter(user_id=user_id, lead_source=request.data['leadsource']).exists():
                self.perform_update(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({'error': 'Updating lead Failed...!!!'})

    def perform_update(self, serializer):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            serializer.save(user=tenant)
        else:
            raise ValidationError("Invalid user_id or associated tenant not found.")


# class LeadCreateView(viewsets.ModelViewSet):
#     # permission_classes = (IsAuthenticated,)
#     queryset = Lead.objects.all()
#     serializer_class = LeadSerializer
#     lookup_field = 'id'


# lead update class
class LeadUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.Lead.objects.all()
    serializer_class = lead_serializers.LeadSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            return super().get_queryset().filter(user=tenant)
        else:
            return []

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        model = lead_models.Lead
        id = self.kwargs['id']
        leadsource = request.data.get('leadsource', '')
        serializer = self.get_serializer(self.get_queryset().get(id=id), data=request.data,
                                         context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        if leadsource:
            if lead_models.LeadSource.objects.filter(user=tenant, lead_source=leadsource).exists():
                perform_update = self.perform_update(serializer, user_id)
                headers = self.get_success_headers(serializer.data)
                sendSignal_updated_record(serializer, user_id, model)

                if perform_update:
                    return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
                else:
                    return Response({'error': 'Updating Lead Failed...!!!'},
                                    headers=headers)
            else:
                return Response({'error': 'Update Failed...!!!'})
        else:
            perform_update = self.perform_update(serializer, user_id)
            headers = self.get_success_headers(serializer.data)
            sendSignal_updated_record(serializer, user_id, model)

            if perform_update:
                return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
            else:
                return Response({'error': 'Updating Lead Failed...!!!'},
                                headers=headers)


    def perform_update(self, serializer, user_id):
        serializer.save(user_id=user_id)
        return True

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


# lead delete class
class LeadDestroyAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.Lead.objects.all()
    serializer_class = lead_serializers.LeadSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            return super().get_queryset().filter(user=tenant)
        else:
            return []

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        id = self.kwargs['id']
        model = lead_models.Lead
        lead = self.get_queryset().get(id=id)
        if lead:
            lead.delete()
            sendSignal_delete_record(user_id, model)

            return Response({'Message': 'Lead Deleted Successfully...!!!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Deleting Lead Failed...!!!'})



class LeadSourceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.LeadSource.objects.all()
    serializer_class = lead_serializers.LeadSourceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            return super().get_queryset().filter(user=tenant)
        else:
            return []

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            lead_source = request.data['lead_source'].strip()
            if lead_models.LeadSource.objects.filter(user_id=tenant.id, lead_source__iexact=lead_source).exists():
                return Response({'error': 'Creating choiceFailed...!!!'})
            # elif LeadSource.objects.filter(lead_source='family' or 'friend' or 'office').exists():
            #     self.perform_create(serializer, user_id)
            #     headers = self.get_success_headers(serializer.data)
            else:
                self.perform_create(serializer, user_id)
                headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'Creating lead choice Failed...!!!'})

    def perform_create(self, serializer, user_id):
        serializer.save(user_id=str(user_id))


    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        model = lead_models.Lead
        id = self.kwargs['id']
        serializer = self.get_serializer(self.get_queryset().get(id=id), data=request.data,
                                         context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        perform_update = self.perform_update(serializer, user_id)
        headers = self.get_success_headers(serializer.data)
        sendSignal_updated_record(serializer, user_id, model)

        if perform_update:
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({'error': 'Updating Lead Source Failed...!!!'},
                            headers=headers)

    def perform_update(self, serializer, user_id):
        serializer.save(user_id=user_id)
        return True

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        id = self.kwargs['id']
        model = lead_models.Lead
        lead = self.get_queryset().get(id=id)
        if lead:
            lead.delete()
            sendSignal_delete_record(user_id, model)

            return Response({'Message': 'Lead Source Deleted Successfully...!!!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Deleting Lead Source Failed...!!!'})

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}



class LeadSourceViewSet1(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.LeadSource.objects.all().order_by('-id')
    serializer_class = lead_serializers.LeadSourceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)

        if tenant:
            return super().get_queryset().filter(user=tenant)
        else:
            return []

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if lead_models.LeadSource.objects.filter(user_id=user_id,
                                                 lead_source__in=['Family', 'Friend', 'Office']).exists():
            return Response({'error': 'Creating choiceFailed...!!!'})
        else:
            lead_sources = [
                lead_models.LeadSource(lead_source='Family', user_id=user_id),
                lead_models.LeadSource(lead_source='Friend', user_id=user_id),
                lead_models.LeadSource(lead_source='Office', user_id=user_id),
            ]

            lead_models.LeadSource.objects.bulk_create(lead_sources)
            return Response({'success': 'Lead Source Created Successfully...!!!'}, status=status.HTTP_201_CREATED)


class LeadsourceDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.LeadSource.objects.all()
    serializer_class = lead_serializers.LeadSourceSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            return super().get_queryset().filter(user=tenant)
        else:
            return []

    def destroy(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        id = self.kwargs['id']
        model = lead_models.Lead
        lead = self.get_queryset().get(id=id)
        if lead:
            lead.delete()
            signals.record_deleted.send(sender=model, user=user_id)
            return Response({'Message': 'Lead Deleted Successfully...!!!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Deleting Lead Failed...!!!'})

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #     return Response({"success": "Custom Field Updated Successfully", "data": serializer.data},
    #                     status=status.HTTP_200_OK)
    #
    # def perform_update(self, serializer):
    #     tenant = tenant_from_request(self.request)
    #     if Sync.objects.filter(tenant_id=tenant.id).exists():
    #         sync = Sync.objects.get(tenant_id=tenant.id)
    #         sync.last_sync = timezone.now()
    #         sync.save()
    #     super().perform_update(serializer)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     return super().partial_update(request, *args, **kwargs)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
    #
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({"success": "Custom Field Deleted Successfully", "id": instance.id},
    #                     status=status.HTTP_200_OK)
    #
    # def perform_destroy(self, instance):
    #     tenant = tenant_from_request(self.request)
    #     device = self.request.data.get("device", None)
    #     instance.device = get_device_object(tenant=tenant, dev_id=device)
    #     instance.is_deleted = True
    #     instance.save()
    #


#
# class LeadCreate(viewsets.ModelViewSet):
#     # permission_classes = (IsAuthenticated,)
#     queryset = Lead.objects.all()
#     serializer_class = LeadSerializer
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         if tenant:
#             lead = Lead.objects.filter(user=tenant)
#             if lead.exists():
#                 return lead
#             else:
#                 raise NotFound({"Alert": "No Lead Found"})
#
#         else:
#             return []
#
#     def create(self, request, *args, **kwargs):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         serializer = self.get_serializer(data=request.data, context={'user_id': user_id})
#
#         print("ser", serializer)
#         if serializer.is_valid(raise_exception=True):
#             model = Lead
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             sendSignal_created_record(serializer, user_id, model)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             return Response({'error': 'Creating lead Failed...!!!'}, status=status.HTTP_400_BAD_REQUEST)
#
#     def perform_create(self, serializer):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         if tenant:
#             serializer.save(user=tenant)
#             return True
#         else:
#             return False
#
#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}
#
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()  # Get the Lead object to be updated
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             self.perform_update(serializer)
#             return Response(serializer.data)
#         else:
#             return Response({'error': 'Updating lead Failed...!!!'}, status=status.HTTP_400_BAD_REQUEST)
#
#     def perform_update(self, serializer):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         if tenant:
#             serializer.save(user=tenant)
#         else:
#             raise ValidationError("Invalid user_id or associated tenant not found.")
#
#
# class LeadUpdateAPI(generics.RetrieveUpdateAPIView):
#     # permission_classes = (IsAuthenticated,)
#     queryset = Lead.objects.all()
#     serializer_class = LeadSerializer
#     lookup_field = 'id'
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         if tenant:
#             return super().get_queryset().filter(user=tenant)
#         else:
#             return []
#
#     def update(self, request, *args, **kwargs):
#         user_id = self.kwargs['user_id']
#         model = Lead
#         id = self.kwargs['id']
#         serializer = self.get_serializer(self.get_queryset().get(id=id), data=request.data)
#         serializer.is_valid(raise_exception=True)
#         perform_update = self.perform_update(serializer)
#         headers = self.get_success_headers(serializer.data)
#         sendSignal_record_updated(serializer, user_id, model)
#
#         if perform_update:
#             return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
#         else:
#             return Response({'error': 'Updating Lead Failed...!!!'}, status=status.HTTP_400_BAD_REQUEST,
#                             headers=headers)
#
#     def perform_update(self, serializer):
#         serializer.save()
#         return True
#
#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}
#
#
# class LeadDestroyAPI(generics.RetrieveDestroyAPIView):
#     # permission_classes = (IsAuthenticated,)
#     queryset = Lead.objects.all()
#     serializer_class = LeadSerializer
#     lookup_field = 'id'
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         if tenant:
#             return super().get_queryset().filter(user=tenant)
#         else:
#             return []
#
#     def destroy(self, request, *args, **kwargs):
#         user_id = self.kwargs['user_id']
#         id = self.kwargs['id']
#         model = Lead
#         lead = self.get_queryset().get(id=id)
#         if lead:
#             lead.delete()
#             signals.signal_record_deleted.send(sender=model, user=user_id)
#             return Response({'Message': 'Lead Deleted Successfully...!!!'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Deleting Lead Failed...!!!'}, status=status.HTTP_400_BAD_REQUEST)
#
#
# import requests
#
# import urllib.request
# from rest_framework.views import APIView
# from rest_framework.response import Response
#
#
# class CheckInternetConnection(APIView):
#     def get(self, request):
#         try:
#             urllib.request.urlopen('http://www.example.com', timeout=2)
#             return Response({'status': 'Internet connection is available.'})
#         except urllib.error.URLError:
#             return Response({'status': 'No internet connection.'})
# @csrf_exempt
# def my_view(request):
#     # Check if the user has an internet connection
#     if request.META.get('HTTP_CONNECTION'):
#         return JsonResponse({'error': 'access internet connection.'}, status=400)
#     else:
#     # Process the API request for users with an internet connection
#     # ...
#
#         return JsonResponse({'message': 'not access.'})


class LeadNoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.LeadNotes.objects.all().order_by('-id')
    serializer_class = lead_serializers.LeadNoteSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            return super().get_queryset().filter(user=tenant)
        else:
            return []

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer, user_id)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'Creating leadnote Failed...!!!'})

    def perform_create(self, serializer, user_id):
        serializer.save(user_id=user_id)

    def update(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        tenant = tenant_from_request_alluser(user_id)
        model = lead_models.Lead
        id = self.kwargs['id']
        serializer = self.get_serializer(self.get_queryset().get(id=id), data=request.data,
                                         context={'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        perform_update = self.perform_update(serializer, user_id)
        headers = self.get_success_headers(serializer.data)
        sendSignal_updated_record(serializer, user_id, model)

        if perform_update:
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        else:
            return Response({'error': 'Updating Lead Failed...!!!'},
                            headers=headers)

    def perform_update(self, serializer, user_id):
        serializer.save(user_id=user_id)
        return True

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class LeadNoteRetrieveView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = lead_models.LeadNotes.objects.all()
    serializer_class = lead_serializers.LeadNoteSerializer
    lookup_field = 'lead_id'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        lead_id = self.kwargs['lead_id']
        tenant = tenant_from_request_alluser(user_id)
        if tenant:
            x = lead_models.LeadNotes.objects.filter(user=tenant)
            if x.exists():
                return lead_models.LeadNotes.objects.filter(lead_id=lead_id).order_by('-id')
            else:
                raise NotFound({"Alert": "No Lead Found"})

        else:
            return []


################                LEAD IMAGE API          ##########################################

# class LeadImageViewSet(viewsets.ModelViewSet):
#     # permission_classes = (IsAuthenticated,)
#     queryset = lead_models.LeadImage.objects.all().order_by('-id')
#     serializer_class = lead_serializers.LeadImageSerializer
#     lookup_field = 'id'
#
#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         if tenant:
#             return super().get_queryset().filter(user=tenant)
#         else:
#             return []
#
#     def create(self, request, *args, **kwargs):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         lead_name = self.request.data.get('lead_name', None)
#         image_file = self.request.data.get('image', None)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             if image_file:
#                 self.perform_create(serializer, user_id)
#                 headers = self.get_success_headers(serializer.data)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#             else:
#                 return Response({'error': 'Creating leadimage Failed...!!!'})
#         else:
#             return Response({'error': 'Creating leadimage Failed...!!!'})
#
#     def perform_create(self, serializer, user_id):
#         lead_name = self.request.data.get('lead_name', None)
#         image_file = self.request.data.get('image', None)
#
#         lead_image_instance = serializer.save(user_id=user_id, image=None)
#
#         if image_file:
#             if lead_name:
#                 filename = f'{lead_name}.jpeg'
#                 print("filename", filename)
#                 lead_image_instance.image.save(filename, ContentFile(image_file.read()), save=False)
#
#             else:
#                 filename = f'{image_file}'
#                 print("filename", filename)
#                 lead_image_instance.image.save(filename, ContentFile(image_file.read()), save=False)
#             lead_image_instance.save()
#
#     def update(self, request, *args, **kwargs):
#         user_id = self.kwargs['user_id']
#         tenant = tenant_from_request_alluser(user_id)
#         model = lead_models.Lead
#         id = self.kwargs['id']
#         lead_name = self.request.data.get('lead_name', None)
#         image_file = self.request.data.get('image', None)
#         serializer = self.get_serializer(self.get_queryset().get(id=id), data=request.data,
#                                          context={'user_id': user_id})
#         serializer.is_valid(raise_exception=True)
#         if image_file:
#             self.perform_update(serializer, user_id)
#             headers = self.get_success_headers(serializer.data)
#             sendSignal_updated_record(serializer, user_id, model)
#             # if perform_update:
#             return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
#         else:
#             return Response({'error': 'Updating Lead Failed...!!!'})
#
#     def perform_update(self, serializer, user_id):
#         lead_name = self.request.data.get('lead_name', None)
#         image_file = self.request.data.get('image', None)
#
#         lead_image_instance = serializer.save(user_id=user_id, image=None)
#
#         if image_file:
#             if lead_name:
#                 filename = f'{lead_name}.jpeg'
#                 print("filename", filename)
#                 lead_image_instance.image.save(filename, ContentFile(image_file.read()), save=False)
#
#             else:
#                 filename = f'{image_file}'
#                 print("filename", filename)
#                 lead_image_instance.image.save(filename, ContentFile(image_file.read()), save=False)
#             lead_image_instance.save()
#
#     def destroy(self, request, *args, **kwargs):
#         user_id = self.kwargs['user_id']
#         id = self.kwargs['id']
#         model = lead_models.LeadImage
#         image = self.get_queryset().get(id=id)
#         if image:
#             image.delete()
#             sendSignal_delete_record(user_id, model)
#
#             return Response({'Message': 'Leadimage Deleted Successfully...!!!'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Deleting Leadimage Failed...!!!'})
#
#     def get_success_headers(self, data):
#         try:
#             return {'Location': str(data[api_settings.URL_FIELD_NAME])}
#         except (TypeError, KeyError):
#             return {}

# class ProfilePicView(APIView):
#     # permission_classes = (IsAuthenticated,)
#
#     # permission_classes = (AllowAny,)
#
#     def get_queryset(self):
#         tenant = tenant_from_request_alluser(self.request)
#         queryset = super().get_queryset().filter(user_id=tenant.id)
#         if queryset is None:
#             return []
#         return queryset
#
#     def post(self, request,*args, **kwargs):
#         user_id = self.kwargs['user_id']
#         tenant_new = tenant_from_request_alluser(user_id)
#         print("tenant_new", tenant_new)
#         lead= lead_models.Lead.objects.get()
#         images = request.data['images']
#         print("images", images)
#         extension = images.split('.')[-1]
#         images = '{}_logo.{}'.format(tenant_new, extension)
#         # fs = S3Boto3Storage(location=get_profile_path(tenant_id=tenant_new.id, fname=""))
#         # filename = fs.save(pic.name, pic)
#         filename = images
#         url = "https://stickynotesandbox.in/api/lead_images/{}".format(tenant_new, filename)
#         ext_obj = lead_models.Image.objects.filter(user_id=tenant_new.id)
#         if ext_obj.exists():
#             user_images = lead_models.Image.objects.get(user_id=tenant_new.id)
#             user_images.images = url
#             user_images.save()
#         else:
#             lead_models.Image.objects.create(images=url, user_id=tenant_new.id)
#         return Response(dict(resp="success", resp_msg="Image added Sucessfully", resp_code="", pic_url=url),
#                         status=status.HTTP_200_OK)
