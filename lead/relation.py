from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.encoding import smart_text, smart_str
from rest_framework import relations

from collections import OrderedDict

from rest_framework.relations import RelatedField


from tenant.utils import tenant_from_request_alluser
from django.utils.translation import gettext_lazy as _


class SharedTenantSlugFilterRelatedField(RelatedField):
    """
    A read-write field that represents the target of the relationship
    by a unique 'slug' attribute.
    """
    default_error_messages = {
        'does_not_exist': _('Object with {slug_name}={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }

    def __init__(self, slug_field=None, **kwargs):
        assert slug_field is not None, 'The `slug_field` argument is required.'
        self.slug_field = slug_field
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        data_request = self.context['user_id']
        print("data_req",data_request)
        tenant = tenant_from_request_alluser(data_request)
        print("tene",tenant.id)
        # leadsource = self.context["request"].data.get("leadsource")
        queryset = self.get_queryset().filter(user_id=tenant.id)
        print("queryset",queryset)
        try:
            print("***", queryset.get(**{self.slug_field: data}))
            return queryset.get(**{self.slug_field: data})
        except ObjectDoesNotExist:
            self.fail('does_not_exist', slug_name=self.slug_field, value=smart_str(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, self.slug_field)
