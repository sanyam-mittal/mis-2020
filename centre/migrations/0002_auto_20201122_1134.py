# Generated by Django 3.1 on 2020-11-22 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('centre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CentreExcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('file', models.FileField(upload_to='excel_files')),
                ('errors', models.PositiveIntegerField(default=0)),
                ('errors_checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='centre',
            name='removed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CentreExcelLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column', models.CharField(max_length=1000)),
                ('row', models.PositiveIntegerField()),
                ('value', models.TextField()),
                ('excel_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centre_error_logs', to='centre.centreexcel')),
            ],
        ),
    ]