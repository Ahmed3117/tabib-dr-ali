# Generated by Django 4.2 on 2023-12-14 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0003_rename_patientprofile_patient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='session_files/', verbose_name='  ملف'),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_file',
            field=models.FileField(blank=True, null=True, upload_to='session_files/', verbose_name='  ملف'),
        ),
    ]
