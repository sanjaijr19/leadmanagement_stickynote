from django.db import models
import datetime
# Create your models here.
from django.db import models
# from djchoices import ChoiceItem, DjangoChoices
from tenant.models import SyncUserAwareModel, AllUserAwareModel


class LeadSource(AllUserAwareModel):

    lead_source = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'LeadSource'

    def __str__(self):
        return self.lead_source




# class Image(AllUserAwareModel):
#     images = models.ImageField(upload_to='images/',null=True, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     edited_on = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = 'Image'
#
#     def __str__(self):
#         return f"Image {self.id}"

# class LeadImage(AllUserAwareModel):
#     lead_name = models.CharField(max_length=30, blank=True, null=True)
#     image = models.ImageField(upload_to='lead_images/',null=True, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     edited_on = models.DateTimeField(auto_now=True)
#     # lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead', null=True)
#
#
#     class Meta:
#         db_table = 'Leadimage'
#
#     def __str__(self):
#         return f"LeadImage {self.id} "

class Lead(AllUserAwareModel):

    LEAD_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Converted', 'Converted'),
        # Add more status choices as needed
    )

    LEAD_SCORE_CHOICES = (
        ('25%', '25%'),
        ('50%', '50%'),
        ('75%', '75%'),
        ('100%', '100%'),
        # Add more score choices as needed
    )

    lead_name = models.CharField(max_length=30, blank=False, null=False)
    lead_image = models.ImageField(upload_to='lead_images/',null=True, blank=True)
    # lead_image = models.ForeignKey(LeadImage, on_delete=models.CASCADE, related_name='leadimage',null=True,blank=True)
    designation = models.CharField(max_length=30, blank=False, null=False)
    leadsource = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, related_name="leadsource", null=True,
                                   blank=True)
    # leadsource = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES)
    # lead_source = models.ForeignKey(Lead_Source, on_delete=models.CASCADE, related_name='lead_source')
    phone_number = models.CharField(max_length=10,null=True, blank=True)
    email_id = models.EmailField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES,null=True, blank=True)
    lead_score = models.CharField(max_length=10, choices=LEAD_SCORE_CHOICES, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Lead'

    def __str__(self):
        return self.lead_name


class LeadNotes(AllUserAwareModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='leadnotes', null=True)
    notes = models.TextField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'Leadnotes'

    def __str__(self):
        return self.notes
