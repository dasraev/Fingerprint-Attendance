# Generated by Django 4.2.1 on 2023-05-28 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fingerprint', '0004_remove_employee_name_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='fingerprint.employee'),
        ),
    ]
