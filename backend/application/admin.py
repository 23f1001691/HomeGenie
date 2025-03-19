from flask import send_file, current_app as app
from application.utils import role_required
from flask_jwt_extended import jwt_required
from celery.result import AsyncResult
from application.celery.tasks import create_csv

@jwt_required()
@role_required(["admin"]) 
@app.get('/admin/get-csv/<task_id>')
def getCSV(task_id):
    
    result = AsyncResult(task_id)
        
    if result.ready() and result.successful():
        filename = result.result
        if filename and filename.startswith('data'):  
            return send_file(f'celery/user-downloads/{filename}'), 200
        else:
            return {'message' : 'Could not export since no data is available'}, 405            
    else:
        return {'message' : 'Task is not ready yet'}, 405

@jwt_required()
@role_required(["admin"]) 
@app.get('/admin/create-csv')
def createCSV():
    task = create_csv.delay()
    return {'task_id' : task.id}, 200 


