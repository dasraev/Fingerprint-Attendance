# Generated by Django 4.2.1 on 2023-05-28 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0008_rename_employee_student'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='employee',
            new_name='student',
        ),
    ]
