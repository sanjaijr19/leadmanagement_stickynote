# Generated by Django 4.2.2 on 2023-07-03 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='lead_source',
            field=models.CharField(choices=[('friend', 'friend'), ('family', 'family'), ('office', 'office'), ('other', 'other')], max_length=20),
        ),
    ]