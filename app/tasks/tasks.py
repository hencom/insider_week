import csv
from openpyxl import load_workbook
from celery import Celery
from datetime import datetime
from pydantic import ValidationError
import json

from models import models
from schemas import schemas

worker = Celery('tasks', broker='redis://redis_iw:6379/0', backend='redis://redis_iw:6379/0')

@worker.task(bind=True)
def read_csv(self, file_path: str) -> None:
    task_id = self.request.get('id')
    models.db.session.query(models.Transaction).delete()
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            try:
                tr = schemas.Transaction(
                    name=row[0], 
                    date=datetime.strptime(row[1], "%m/%d/%Y"), 
                    graph1=row[2], 
                    graph2=row[3], 
                    graph3=row[4]
                    )
                tr_db = models.Transaction(**tr.dict())
                models.db.session.add(tr_db)

            except ValidationError as e:
                models.db.session.rollback()
                t = models.Task(task_is=task_id, data=e.json())
                models.db.session.add(t)
                models.db.session.commit()
                raise
            except IndexError as e:
                models.db.session.rollback()
                t = models.Task(task_is=task_id, data=json.dumps({'error': 'index error'}))
                models.db.session.add(t)
                models.db.session.commit()
                raise

    t = models.Task(task_is=task_id, data=json.dumps({'result': 'OK'}))
    models.db.session.add(t)
    models.db.session.commit()

@worker.task(bind=True)
def read_exel(self, file_path: str) -> None:
    task_id = self.request.get('id')
    wb = load_workbook(filename=file_path, read_only=True)
    models.db.session.query(models.Transaction).delete()
    ws = wb.active
    for row in ws.rows:
        if type(row[1].value) is str:
            dt = datetime.strptime(row[1].value, "%m/%d/%Y")
        else:
            dt = row[1].value
        try:
            tr = schemas.Transaction(
                    name=row[0].value, 
                    date=dt, 
                    graph1=row[2].value, 
                    graph2=row[3].value, 
                    graph3=row[4].value
                )
            tr_db = models.Transaction(**tr.dict())
            models.db.session.add(tr_db)
    
        except ValidationError as e:
            models.db.session.rollback()
            wb.close()
            t = models.Task(task_is=task_id, data=e.json())
            models.db.session.add(t)
            models.db.session.commit()
            raise
    
    wb.close()
    t = models.Task(task_is=task_id, data=json.dumps({'result': 'OK'}))
    models.db.session.add(t)
    models.db.session.commit()

