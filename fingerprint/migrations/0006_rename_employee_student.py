# Generated by Django 4.2.1 on 2023-05-28 22:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fingerprint', '0005_alter_attendance_employee'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='Student',
        ),
    ]