# Generated by Django 4.2 on 2024-01-12 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0011_sessionprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionprice',
            name='new_session_price',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name=' سعر الكشف الجديد'),
        ),
        migrations.AlterField(
            model_name='sessionprice',
            name='return_session_price',
            field=models.IntegerField(blank=True, default=1, null=True, verbose_name=' سعر اعادة الكشف'),
        ),
    ]
