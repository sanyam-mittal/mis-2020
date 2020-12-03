from celery import shared_task
import re
from django.shortcuts import get_object_or_404
from . import models
from centre import models as centre_models
import pandas as pd

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
    excel = get_object_or_404(models.CentreExcel, pk=id)
    try:
        data = pd.read_excel(str(url))
        columns = list(data.columns)
        for index, row in data.iterrows():
            for idx, col in enumerate(columns):
                x = re.match(str(regex_val[col]), str(row[col]))
                if not x:
                    models.CentreExcelLog.objects.create(excel_file=excel, column=col, row=idx, value=str(row[col]))
                    excel.errors += 1
        excel.errors_checked = True
        excel.save()
        if excel.errors == 0:
            insert_centre_excel.delay(url, id)
        return True
    except Exception as err:
        models.CentreExcel.objects.create(excel_file=excel, column="NA", row=0, value=err)
        excel.errors += 1
        excel.errors_checked = True
        excel.save()
        return False


@shared_task()
def insert_centre_excel(url, id):
    excel = get_object_or_404(models.CentreExcel, pk=id)
    try:
        data = pd.read_excel(str(url))
        for index, row in data.iterrows():
            createCentre(row)
        return True

    except Exception as err:
        excel.errors += 1
        excel.save()
        models.CentreExcelLog.objects.create(excel_file=excel, column="NA", row=0, value=err)
        return False


def createCentre(row):
    try:
        if centre_models.Centre.objects.filter(code=row['Venue Code'], removed=False).exists():
            centre = centre_models.Centre.objects.filter(code=row['Venue Code'], removed=False)[0]
        else:
            centre = centre_models.Centre.objects.create(ssc_region=row['SSC Region'],
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
        return True
    except Exception as err:
        print(err)
        pass
