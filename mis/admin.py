from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Excel)
admin.site.register(models.ExcelLog)
admin.site.register(models.Project)
admin.site.register(models.ProjectDetail)
admin.site.register(models.ClientProjectMap)
