from time import sleep
import botocore
from celery import shared_task
import re
from datetime import date, datetime
from django.shortcuts import get_object_or_404
from django.utils import timezone

from . import models
from centre import models as centre_models
import pandas as pd


@shared_task()
def sleepy():
    sleep(10)
    return None


regex_val = {}
regex_val['Client Name'] = '[a-zA-Z().\']+$'
regex_val['Project Code'] = '[A-Za-z0-9,-.\()=/]+$'
regex_val['Exam Start Date'] = '[A-Za-z 0-9,-.:/-]+$'
regex_val['Exam End Date'] = '[A-Za-z 0-9,-.:/-]+$'
regex_val['SSC Region'] = '[a-zA-Z()]+$'
regex_val['Zone'] = '[a-zA-Z0-9_ ]+$'
regex_val['State'] = '[a-zA-Z ()]+$'
regex_val['City'] = '[a-zA-Z()]+$'
regex_val['Venue Code'] = '^\d+$'
regex_val['Venue Name'] = '[A-Za-z0-9 ,-.\()=/]+$'
regex_val['Address'] = '[A-Za-z 0-9,-.\()=/:]+$'
regex_val['Pincode'] = '^\d+$'
regex_val['Center Contact Name'] = '^[ a-zA-Z().\']+$'
regex_val['Center Contact Number'] = '^\d{10}$'
regex_val['Exam Date'] = '[A-Za-z 0-9,-.:/-]+$'
regex_val['Shift 1'] = '^\d+$'
regex_val['Shift 2'] = '^\d+$'
regex_val['Shift 3'] = '^\d+$'
regex_val['Shift 1 timings'] = '[A-Za-z0-9,-.:/-]+$'
regex_val['Shift 2 timings'] = '[A-Za-z0-9,-.:/-]+$'
regex_val['Shift 3 timings'] = '[A-Za-z0-9,-.:/-]+$'
regex_val['Max Count'] = '^\d+$'
regex_val['Total Count'] = '^\d+$'


@shared_task()
def validate_excel(url, id):
    excel = get_object_or_404(models.Excel, pk=id)
    try:
        data = pd.read_excel(str(url))
        columns = list(data.columns)
        for index, row in data.iterrows():
            for idx, col in enumerate(columns):
                x = re.match(str(regex_val[col]), str(row[col]))
                if not x:
                    models.ExcelLog.objects.create(excel_file=excel, column=col, row=idx, value=str(row[col]))
                    excel.errors += 1
        excel.errors_checked = True
        excel.save()
        if excel.errors == 0:
            if excel.update_file:
                delete_prev_projects.delay(url, id)
            else:
                insert_excel.delay(url, id)
        return True
    except Exception as err:
        excel.errors += 1
        excel.errors_checked = True
        excel.save()
        models.ExcelLog.objects.create(excel_file=excel, column="NA", row=0, value=err)
        return False


@shared_task()
def insert_excel(url, id):
    excel = get_object_or_404(models.Excel, pk=id)
    try:
        data = pd.read_excel(str(url))
        for index, row in data.iterrows():
            createProject(row)
        return True

    except Exception as err:
        excel.errors += 1
        excel.save()
        models.ExcelLog.objects.create(excel_file=excel, column="NA", row=0, value=err)
        return False


@shared_task()
def delete_prev_projects(url, id):
    try:
        data = pd.read_excel(str(url))
        for index, row in data.iterrows():
            project_code = row['Project Code']
            models.Project.objects.filter(removed=False, code__icontains=str(project_code)).update(removed=True)
        insert_excel(url, id)
        return True

    except Exception as err:
        print("#######################################################################################")
        print(err)
        return False


def createProject(row):
    try:
        if centre_models.Centre.objects.filter(code=row['Venue Code'], removed=False).exists():
            centre = centre_models.Centre.objects.filter(code=row['Venue Code'], removed=False)[0]
        else:
            centre = centre_models.Centre.objects.create(
                                                         ssc_region=row['SSC Region'],
                                                         zone=row['Zone'].lower(),
                                                         state=row['State'],
                                                         city=row['City'],
                                                         code=row['Venue Code'],
                                                         name=row['Venue Name'],
                                                         address=row['Address'],
                                                         pincode=row['Pincode'],
                                                         centre_type='new'
                                                         )
            operator = centre_models.Operator.objects.create(centre=centre)
        if models.ClientProjectMap.objects.filter(client__icontains=row['Client Name']).exists():
            pm_map = models.ClientProjectMap.objects.filter(client__icontains=row['Client Name'])[0]
            pm = pm_map.pm
        else:
            pm = None

        project = models.Project.objects.create(
            centre=centre,
            code=row['Project Code'],
            client_name=row['Client Name'],

            exam_start=row['Exam Start Date'],
            exam_end=row['Exam End Date'],
            exam_on=row['Exam Date'],

            shift1=row['Shift 1'],
            shift1_timing=row['Shift 1 timings'],
            shift2=row['Shift 2'],
            shift2_timing=row['Shift 2 timings'],
            shift3=row['Shift 3'],
            shift3_timing=row['Shift 3 timings'],
            max_count=row['Max Count'],
            total_count=row['Total Count'],
            pm=pm,
        )
        projectdetail = models.ProjectDetail.objects.create(project=project)
    except Exception as err:
        print(err)
        pass
