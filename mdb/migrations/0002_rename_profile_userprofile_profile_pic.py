# Generated by Django 5.0.1 on 2024-01-31 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mdb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile',
            new_name='profile_pic',
        ),
    ]