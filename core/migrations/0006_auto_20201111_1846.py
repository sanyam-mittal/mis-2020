# Generated by Django 2.2 on 2020-11-11 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201111_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='designation',
            field=models.CharField(blank=True, choices=[('MIS', 'MIS'), ('ZM', 'ZM'), ('PM', 'PM'), ('PC', 'PC')], max_length=30, null=True),
        ),
    ]