from django.db import models
from . import tasks
# Create your models here.


class NotRemovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(removed=False)


class Centre(models.Model):

    zone = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    code = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    address = models.TextField()
    pincode = models.PositiveIntegerField()
    ssc_region = models.CharField(max_length=1000)
    centre_type = models.CharField(max_length=1000)

    removed = models.BooleanField(default=False)
    objects = models.Manager()
    av_objects = NotRemovedManager()

    def __str__(self):
        return self.code + '-' + self.name


class Operator(models.Model):
    centre = models.OneToOneField(Centre, on_delete=models.CASCADE, related_name='operator')
    first_name = models.CharField(max_length=1000, blank=True, null=True)
    last_name = models.CharField(max_length=1000, blank=True, null=True)
    contact_number = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    hq = models.CharField(max_length=1000, blank=True, null=True)
    govt_id_proof_type = models.CharField(max_length=1000, blank=True, null=True)
    govt_id_proof_no = models.CharField(max_length=1000, blank=True, null=True)
    father_name = models.CharField(max_length=1000, blank=True, null=True)
    mother_name = models.CharField(max_length=1000, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        flag = 0
        if self.first_name==None or self.first_name=='':
            flag = 1
        if self.last_name==None or self.last_name=='':
            flag = 1
        if self.contact_number==None:
            flag = 1
        if self.email==None:
            flag = 1
        if self.dob==None:
            flag = 1
        if self.hq==None or self.hq=='':
            flag = 1
        if self.govt_id_proof_type==None or self.govt_id_proof_type=='':
            flag = 1
        if self.govt_id_proof_no==None or self.govt_id_proof_no=='':
            flag = 1
        if self.father_name==None or self.father_name=='':
            flag = 1
        if self.mother_name is None or self.mother_name== '':
            flag = 1
        if flag:
            self.status = False
        else:
            self.status = True
        super().save(*args, **kwargs)


class CentreExcel(models.Model):
    name = models.CharField(max_length=1000, default="", null=True, blank=True)
    file = models.FileField(upload_to="excel_files")
    errors = models.PositiveIntegerField(default=0)
    errors_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        excel = self.file
        self.name = self.file.name
        super().save(*args, **kwargs)
        if not self.errors_checked:
            tasks.validate_excel(excel.url, self.id)

    def __str__(self):
        return str(self.name)


class CentreExcelLog(models.Model):
    excel_file = models.ForeignKey(CentreExcel, on_delete=models.CASCADE, related_name="centre_error_logs")
    column = models.CharField(max_length=1000)
    row = models.PositiveIntegerField()
    value = models.TextField()

    def __str__(self):
        return self.value + self.column + str(self.row)
