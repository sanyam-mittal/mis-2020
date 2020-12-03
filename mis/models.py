from datetime import datetime
from django.utils import timezone
from django.db import models
from . import tasks
from core import models as core_models
from centre import models as centre_models


class Excel(models.Model):
    name = models.CharField(max_length=1000, default="", null=True, blank=True)
    file = models.FileField(upload_to="excel_files")
    update_file = models.BooleanField(default=False)
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


class ExcelLog(models.Model):
    excel_file = models.ForeignKey(Excel, on_delete=models.CASCADE, related_name="logs")
    column = models.CharField(max_length=1000)
    row = models.PositiveIntegerField()
    value = models.TextField()

    def __str__(self):
        return self.value + self.column + str(self.row)


class NotRemovedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(removed=False)


class ClientProjectMap(models.Model):
    client = models.CharField(max_length=1000)
    pm = models.ForeignKey(core_models.User, on_delete=models.DO_NOTHING, related_name="client_names")

    def __str__(self):
        return self.client + '-' + str(self.pm)


class Project(models.Model):
    insert_ts = models.DateTimeField(default=timezone.now)
    centre = models.ForeignKey(centre_models.Centre, on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    client_name = models.CharField(max_length=1000)
    code = models.CharField(max_length=5000)

    exam_start = models.DateField()
    exam_end = models.DateField()
    exam_on = models.DateField()

    shift1 = models.CharField(max_length=1000)
    shift1_timing = models.TimeField()
    shift2 = models.CharField(max_length=1000)
    shift2_timing = models.TimeField()
    shift3 = models.CharField(max_length=1000)
    shift3_timing = models.TimeField()

    max_count = models.IntegerField()
    total_count = models.IntegerField()

    pc = models.ForeignKey(core_models.User, on_delete=models.DO_NOTHING, related_name="project_pc", null=True,
                           blank=True, default=None)
    pm = models.ForeignKey(core_models.User, on_delete=models.DO_NOTHING, related_name="project_pm", null=True,
                           blank=True, default=None)
    zm = models.ForeignKey(core_models.User, on_delete=models.DO_NOTHING, related_name="project_zm", null=True,
                           blank=True, default=None)

    removed = models.BooleanField(default=False)
    removed_ts = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    av_objects = NotRemovedManager()

    def __str__(self):
        return str(self.centre) + '-' + self.client_name

    class Meta:
        ordering = ['-insert_ts']


class ProjectDetail(models.Model):

    # centre details
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='project', blank=True, null=True)

    prev_cam_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    last_exam_observations = models.TextField(blank=True, null=True)
    model = models.CharField(max_length=1000, blank=True, null=True)
    rate = models.PositiveIntegerField(blank=True, null=True)
    centre_type_choices = (
        ("old", "old"),
        ("new", "new"),
        ("permanent_installed", "permanent installed"),
        ("puneet_mittal", "puneet mittal"),
        ("rahul_bansal", "rahul bansal"),
    )
    centre_type = models.CharField(max_length=1000, choices=centre_type_choices, blank=True, null=True)
    centre_open_time = models.TimeField(blank=True, null=True)
    centre_close_time = models.TimeField(blank=True, null=True)

    # installation status at centre
    venue_head_contacted_by_vendor = models.BooleanField(default=False, blank=True, null=True)
    centre_visited_by_vendor = models.BooleanField(default=False, blank=True, null=True)
    disputed_centre = models.BooleanField(default=False, blank=True, null=True)
    wiring_status_choices = (
        ("started", "started"),
        ("completed", "completed")
    )
    wiring_status = models.CharField(max_length=1000, choices=wiring_status_choices, blank=True, null=True)
    camera_status = models.CharField(max_length=1000, choices=wiring_status_choices, blank=True, null=True)
    dvr_status = models.BooleanField(default=False, blank=True, null=True)
    live_feed_operational_choices = (
        ("yes", "yes"),
        ("no", "no"),
        ("offline", "offline")
    )
    live_feed_operational = models.CharField(max_length=1000, choices=wiring_status_choices, blank=True, null=True)
    comments_for_installation = models.TextField(blank=True, null=True)
    installation_status_choices = (
        ("disputed", "disputed"),
        ("work_in_progress", "work in progress"),
        ("installation_complete", "installation complete"),
        ("centre_live", "centre live"),
        ("offline_live", "offline live"),
        ("pending", "pending"),
    )
    installation_status = models.CharField(max_length=1000, choices=installation_status_choices, blank=True, null=True)
    total_camera_installed = models.PositiveIntegerField(blank=True, null=True)
    total_camera_used = models.PositiveIntegerField(blank=True, null=True)
    total_camera_count = models.PositiveIntegerField(blank=True, null=True)
    platform_choices = (
        ("DSS", "DSS"),
        ("hik_central", "hik central"),
        ("other", "other"),
    )
    platform = models.CharField(max_length=1000, choices=installation_status_choices, blank=True, null=True)

    # QC Details
    qc_status_choices = (
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('pending_at_dm', 'Pending at DM'),
        ('pending', 'Pending')
    )
    ready_for_qc = models.BooleanField(default=False, blank=True, null=True)
    qc_date = models.DateField(blank=True, null=True)
    qc_time_slot = models.CharField(max_length=1000, blank=True, null=True)
    pc_comments_for_qc = models.TextField(blank=True, null=True)
    qc_status = models.CharField(max_length=1000, choices=qc_status_choices, blank=True, null=True)
    reason_qc = models.TextField(blank=True, null=True)
    count_of_qc_requests = models.PositiveIntegerField(default=0)
    qc_percentage_choices = (
        ("0", "0"),
        ("25", "25"),
        ("50", "50"),
        ("100", "100"),
    )
    qc_percentage = models.CharField(max_length=100, choices=qc_percentage_choices, blank=True, null=True)

    # mock details
    mock_status_choices = (
        ('MP', 'Mock Pass'),
        ('MF', 'Mock Fail'),
        ('PAD', 'Pending at DM'),
        ('MP', 'Mock Pending')
    )
    ready_for_mock = models.BooleanField(default=False)
    mock_date = models.DateField(blank=True, null=True)
    mock_status = models.CharField(max_length=1000, choices=mock_status_choices, blank=True, null=True)
    mock_time_slot = models.TimeField(blank=True, null=True)
    pc_comments_for_mock = models.TextField(blank=True, null=True)
    reason_mock = models.TextField(blank=True, null=True)
    count_of_mock_requests = models.PositiveIntegerField(default=0)
    mock_percentage_choices = (
        ("", ""),
        ("0", "0"),
        ("25", "25"),
        ("50", "50"),
        ("100", "100"),
    )
    mock_percentage = models.CharField(max_length=1000, choices=mock_percentage_choices, blank=True, null=True)
