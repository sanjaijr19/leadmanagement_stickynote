# from django.dispatch import receiver
# import datetime
# from django.db.models.signals import post_save
#
#
# from lead.models import Lead
# from policies import signals
# from policies import utils
# from lead import utils
# from policies import models as policy_model
#
#
# @receiver(signals.record_created, sender=Lead)
# def LeadDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Lead",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Lead has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushLeadDataMsg(user, data_message)
#
#
#
# @receiver(signals.record_updated, sender=Lead)
# def LeadDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Lead",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Lead has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushLeadDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=Lead)
# def LeadDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Lead",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Lead has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushLeadDataMsg(user, data_message)
#
# @receiver(signals.record_created, sender=policy_model.Policy)
# def policyDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Policy",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Policy has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
#
# @receiver(signals.record_updated, sender=policy_model.Policy)
# def policyDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Policy",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Policy has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Policy)
# def policyDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Policy",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Policy has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.Client)
# def clientDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Client",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Client has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.Client)
# def clientDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Client",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Client has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Client)
# def clientDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Client",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Client has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.Birthday)
# def birthdayDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Birthday",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Birthday has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.Birthday)
# def birthdayDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Birthday",
#         "Request": "POST",
#         "Status": "200_OK",
#         "Message": "Birthday has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Birthday)
# def birthdayDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Birthday",
#         "Request": "POST",
#         "Status": "204_NO_CONTENT",
#         "Message": "Birthday has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.Contact)
# def contactDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Contact",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Contact has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.Contact)
# def contactDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Contact",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Contact has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Contact)
# def contactDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Contact",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Contact has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.ContactGroup)
# def contactGroupDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "ContactGroup",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New ContactGroup has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.ContactGroup)
# def contactGroupDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "ContactGroup",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "ContactGroup has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.ContactGroup)
# def contactGroupDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "ContactGroup",
#         "Request": "DELETED",
#         "Status": "204_NO_CONTENT",
#         "Message": "ContactGroup has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.LapsedPolicy)
# def lapsedPolicyDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "LapsedPolicy",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New LapsedPolicy has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.LapsedPolicy)
# def lapsedPolicyDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "LapsedPolicy",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "LapsedPolicy has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.LapsedPolicy)
# def lapsedPolicyDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "LapsedPolicy",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "LapsedPolicy has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.Reminder)
# def reminderDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Reminder",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Reminder has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.Reminder)
# def reminderDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Reminder",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Reminder has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Reminder)
# def reminderDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Reminder",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Reminder has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.Template)
# def templateDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Template",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Template has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.Template)
# def templateDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Template",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Template has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Template)
# def templateDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Template",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Template has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_created, sender=policy_model.Note)
# def noteDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Note",
#         "Request": "POST",
#         "Status": "201 Created",
#         "Message": "New Note has been Created...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_updated, sender=policy_model.Note)
# def noteDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Note",
#         "Request": "PUT",
#         "Status": "200_OK",
#         "Message": "Note has been Updated...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
# @receiver(signals.record_deleted, sender=policy_model.Note)
# def noteDataMsg(sender, user, **kwargs):
#     print("Signal Received from sender", sender)
#     data_message = {
#         "Model": "Note",
#         "Request": "DELETE",
#         "Status": "204_NO_CONTENT",
#         "Message": "Note has been Deleted...!!!",
#         "Received_at": f"{datetime.datetime.now()}"
#     }
#     utils.pushDataMsg(user, data_message)
#
#
#
#
#
