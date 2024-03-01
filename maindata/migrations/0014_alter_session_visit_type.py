# Generated by Django 4.2 on 2024-01-23 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maindata', '0013_patentpay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='visit_type',
            field=models.CharField(blank=True, choices=[('N', 'جديد'), ('R', 'اعادة')], default='N', max_length=10, null=True, verbose_name=' نوع الزيارة'),
        ),
    ]