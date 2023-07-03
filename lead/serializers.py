from rest_framework import serializers

from .models import Lead


# serializers.py
from rest_framework import serializers
from .models import Lead

class LeadSerializer(serializers.ModelSerializer):
    # lead_source_other = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Lead
        fields = '__all__'
    #
    # def create(self, validated_data):
    #     lead_source_other = validated_data.pop('lead_source_other', None)
    #     if lead_source_other:
    #         validated_data['lead_source'] = lead_source_other
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     lead_source_other = validated_data.pop('lead_source_other', None)
    #     if lead_source_other:
    #         validated_data['lead_source'] = lead_source_other
    #     return super().update(instance, validated_data)



