from celery import shared_task
from application.models import ServiceRequest
import flask_excel
import os

@shared_task(bind = True, ignore_result = False)
def create_csv(self):
    resource = ServiceRequest.query.filter_by(status_updated_by='Professional',status='Closed').all()
    task_id = self.request.id
    
    if not resource:
        return "No resources available for export"
    
    try:
        filename = f'data_{task_id}.csv'
        column_names = [column.name for column in ServiceRequest.__table__.columns]
        csv_out = flask_excel.make_response_from_query_sets(query_sets = resource, column_names = column_names, file_type='csv' )
        file_path = os.path.join('..', 'backend', 'application', 'celery', 'user-downloads', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(csv_out.data)
        return filename
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None