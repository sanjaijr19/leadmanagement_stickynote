from django.db import models

from users.models import SyncUser,AllUser


class SyncUserAwareModel(models.Model):
    user = models.ForeignKey(SyncUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AllUserAwareModel(models.Model):
    user = models.ForeignKey(AllUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True