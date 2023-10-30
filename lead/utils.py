from users import models as user_models
from pyfcm import FCMNotification
# from lead import signals
# from policies import signals
from policies import signals
# from lead import signals
from tenant.utils import tenant_from_request_alluser
from lead.models import Lead


def pushLeadDataMsg(user_id, data_message):
    device_id = []

    devices = user_models.AllUserDevice.objects.filter(duser=user_id)

    for device in devices:
        device_id.append(device.dfcm)

    push_service = FCMNotification(
        api_key='AAAAS3A1J6A:APA91bFpSsa8_LdIV7VHy5w7PgPatIMkvDCmK31KDjFHel370vEH9MCMmlp65fvpFWC1aBjTtQ1lVd0MXERhwN'
                '-EjOdg4vngABqlGQUlrHURBCb9kd0EABy9Kjm0r_FgLzhrAOlouqRw')

    registration_id = device_id
    print("*******", registration_id)
    result = push_service.multiple_devices_data_message(registration_ids=registration_id, data_message=data_message)
    print("result", result)
    print(data_message, result)


def sendSignal_created_record(serializer, user_id, model):
    tenant = tenant_from_request_alluser(user_id)
    if len(serializer.validated_data) >= 1 and tenant:
        signals.record_created.send(sender=model, user=user_id)
        print("sendSignal_created_record", signals.record_created.send(sender=model, user=user_id))


def sendSignal_updated_record(serializer, user_id, model):
    tenant = tenant_from_request_alluser(user_id)
    if len(serializer.validated_data) >= 1 and tenant:
        signals.record_updated.send(sender=model, user=user_id)

def sendSignal_delete_record(user_id, model):
    tenant = tenant_from_request_alluser(user_id)
    if tenant:
        signals.record_deleted.send(sender=model, user=user_id)
