# Generated by Django 3.2.4 on 2023-08-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0002_alter_lead_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
