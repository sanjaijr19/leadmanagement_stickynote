from rest_framework.exceptions import NotFound

from users import models as user_models


def tenant_from_request(user_id):
    try:
        tenant = user_models.SyncUser.objects.get(id=user_id)
        return tenant
    except user_models.SyncUser.DoesNotExist:
        print("not exist")
        return False


def tenant_from_request_alluser(user_id):
    try:
        tenant = user_models.AllUser.objects.get(id=user_id)
        print("tenant", tenant)
        return tenant
    except user_models.AllUser.DoesNotExist:
        print("not exist")
        raise NotFound({"Alert": "user not Found"})