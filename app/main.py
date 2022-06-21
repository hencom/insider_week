import os
from asgiref.wsgi import WsgiToAsgi
from werkzeug.utils import secure_filename
from flask import abort, jsonify

from core.app import app
from models import models
from tasks.tasks import worker
from schemas import schemas
from flask_openapi3 import Tag


UPLOAD_FOLDER = '/media'
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
asgi_app = WsgiToAsgi(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(406)
def resource_not_found(e):
    return jsonify(error=str(e)), 406


file_upload_tag = Tag(name='File', description='Upload file')
@app.post('/insider_week/file', tags=[file_upload_tag])
def upload_new_file(form: schemas.UploadFileForm):
    print(form.file.filename)
    filename = secure_filename(form.file.filename)
    ext = filename.split(".")[-1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    form.file.save(file_path)
    if ext == 'xlsx':
        task = worker.send_task('tasks.tasks.read_exel', kwargs={'file_path': file_path})
    elif ext == 'csv':
        task = worker.send_task('tasks.tasks.read_csv', kwargs={'file_path': file_path})
    else:
        abort(406)
    return {"code": 200, "task": task.id}, 200


tasks_tag = Tag(name='Tasks', description='Tasks results')
@app.get('/insider_week/tasks', tags=[tasks_tag])
def get_task_result_list(query: schemas.Pagination):
    task_list = models.Task.query.offset(query.offset).limit(query.limit).all()
    m = schemas.TaskList(task_list=task_list)
    return m.dict()


transaction_list_tag = Tag(name='Transactions', description='Transaction list')
@app.get('/insider_week/transactions', tags=[transaction_list_tag])
def get_transaction_list(query: schemas.Pagination):
    transaction_list = models.Transaction.query.offset(query.offset).limit(query.limit).all()
    m = schemas.TransactionList(transaction_list=transaction_list)
    return m.dict()

transaction_tag = Tag(name='Transaction', description='Transaction by id')
@app.get('/insider_week/transactions/<int:id>', tags=[transaction_tag])
def get_transaction(path: schemas.ById):
    transaction = models.db.session.query(models.Transaction).filter(models.Transaction.id == path.id).first()
    if not transaction:
        abort(404)
    m = schemas.Transaction.from_orm(transaction)
    return m.dict()

task_tag = Tag(name='Task', description='Task by id')
@app.get('/insider_week/task/<int:id>', tags=[task_tag])
def get_task(path: schemas.ById):
    task = models.db.session.query(models.Task).filter(models.Task.id == path.id).first()
    if not task:
        abort(404)
    m = schemas.Task.from_orm(task)
    return m.dict()
