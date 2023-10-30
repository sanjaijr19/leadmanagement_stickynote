import datetime

from django.core.files.storage import default_storage
from django import forms
from django.utils.text import get_valid_filename
from rest_framework import serializers
# from .models import Lead
from django.shortcuts import get_object_or_404
from users.models import AllUser
# from .models import Lead, LeadSource, LeadNotes

# serializers.py
from rest_framework import serializers
from . import models as lead_models
from .relation import SharedTenantSlugFilterRelatedField


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


# class LeadSerializer(serializers.ModelSerializer):
#     # lead_image = Base64ImageField(
#     #     max_length=None, use_url=True,
#     # )
#
#     class Meta:
#         model = lead_models.Lead
#         fields = 'id', 'lead_name', 'lead_image', 'designation', 'leadsource', 'phone_number', 'email_id', 'address', 'lead_status', 'lead_score', 'created_on', 'user'
#         read_only_fields = ('user',)
#

class LeadSourceSerializer(serializers.ModelSerializer):
    # other_lead_source = serializers.CharField(max_length=20)
    # lead_source = serializers.ChoiceField(choices=LeadSource.LEAD_SOURCE_CHOICES)
    lead_source_id = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)


    class Meta:
        model = lead_models.LeadSource
        fields = ('id', 'lead_source', 'lead_source_id', 'lead_source', 'created_at')
        read_only_fields = ('created_at', 'lead_source_id')

    def get_lead_source_id(self, obj):
        return obj.id


# For Leadsource category
# class LeadSourceSerializer1(serializers.ModelSerializer):
#
#
#     class Meta:
#         model = lead_models.LeadSource
#         fields = ('id', 'lead_source', 'created_at')
#         read_only_fields = ('lead_source', 'created_at','lead_source_id')

# class LeadImageSerializer(serializers.ModelSerializer):
#     # image = serializers.ImageField(required=False, allow_empty_file=True)
#
#
#     class Meta:
#         model = lead_models.LeadImage
#         fields = ('id', 'image', 'created_on', 'edited_on', 'user')
#         read_only_fields = ('user','created_on','edited_on')
#
#     # def get_image_id(self, obj):


class LeadImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if data == "":
            return None
        return super().to_internal_value(data)

class CustomDateField(serializers.DateField):
    def to_internal_value(self, data):
        if data == '':
            # If the input data is an empty string, return None
            return None
        return super().to_internal_value(data)

class LeadSerializer(serializers.ModelSerializer):
    dob = CustomDateField(allow_null=True, required=False)
    leadsource = SharedTenantSlugFilterRelatedField(queryset=lead_models.LeadSource.objects.all(),
                                                    slug_field='lead_source', required=False, allow_null=True)
    # lead_image = Base64ImageField(max_length=None,use_url=True, allow_empty_file=True,required=False)
    lead_image = LeadImageField(required=False)
    created_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    edited_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # created_on = serializers.DateTimeField(format="%Y-%m-%d %I:%M:%S %p", read_only=True)
    class Meta:
        model = lead_models.Lead
        fields = 'id', 'lead_name', 'lead_image', 'designation', 'leadsource', 'leadsource_id', 'phone_number', 'email_id','dob', 'address', 'lead_status', 'lead_score', 'created_on', 'edited_on', 'user'
        read_only_fields = ('user', 'created_on', 'edited_on')

    # def get_created_on(self, obj):
    #        tz_in = pytz.timezone('Asia/Kolkata')
    #        return obj.created_on.astimezone(tz=tz_in).strftime('%Y-%m-%d %H:%M:%S')


class Leadserializer1(serializers.ModelSerializer):

    class Meta:
        model = lead_models.Lead
        fields = 'id', 'lead_name', 'lead_image', 'designation', 'leadsource', 'leadsource_id', 'phone_number', 'email_id','dob', 'address', 'lead_status', 'lead_score', 'created_on', 'edited_on', 'user'

class LeadNoteSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    edited_on = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = lead_models.LeadNotes
        fields = ('id', 'lead', 'notes', 'created_on', 'edited_on', 'user')
        read_only_fields = ('created_at', 'edited_on', 'user')
