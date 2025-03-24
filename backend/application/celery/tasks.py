from celery import shared_task
import flask_excel
import os
from weasyprint import HTML
from io import BytesIO
from application.models import ServiceRequest, Professional, Customer, Admin
from datetime import datetime
from application.celery.scheduled_mail import send_mail_with_pdf, send_mail
from flask import render_template

@shared_task(bind = True, ignore_result = False)
def create_csv(self):
    resource = ServiceRequest.query.all()
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
    
@shared_task(ignore_result = True)
def new_req_checks():
    professionals = Professional.query.all()
    for professional in professionals:
        service_requests = ServiceRequest.query.filter_by(professional_id=professional.id, status="Requested").all()

        if service_requests:
            recipient = professional.user.email
            subject = "Daily Reminder : New requests"
            url = 'http://localhost:8080/sign-in'
            body = render_template('daily_activity.html', name=professional.name, url=url, count=len(service_requests))
            send_mail(recipient, subject, body, is_html=True)
            return 'Mail is sent'
        
@shared_task(ignore_result = True)
def new_prof_checks():
    professionals = Professional.query.filter_by(status="Unapproved").all()
    admin = Admin.query.first()
    if professionals:
        recipient = admin.user.email
        subject = "Daily Reminder : New service professional"
        url = 'http://localhost:8080/sign-in'
        body = render_template('daily_activity.html', name='Admin', url=url, count=len(professionals))
        send_mail(recipient, subject, body, is_html=True)
        return 'Mail is sent'
            
@shared_task(ignore_result = True)
def send_monthly_report():
    today = datetime.today().date()
    month, year = datetime.today().month, datetime.today().year
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    customers = Customer.query.all()

    for customer in customers:
        service_requests = ServiceRequest.query.filter(
            ServiceRequest.customer_id == customer.id,
            ServiceRequest.date_of_request.between(datetime(prev_year, prev_month, 1).date(), today)
        ).all()

        recipient=customer.user.email

        prev_month = datetime(prev_year, prev_month, 1).strftime('%B') 
        subject="Monthly Activity Report",

        if service_requests:
            req_count = sum(1 for request in service_requests if request.status=='Requested')
            prog_count = sum(1 for request in service_requests if request.status=='Assigned')
            closed_count = sum(1 for request in service_requests if (request.status=='Closed' or request.status=='Paid'))
            rej_count = sum(1 for request in service_requests if request.status== 'Rejected')
      
            report = render_template('report.html', service_requests=service_requests, customer=customer, 
                                     month=prev_month, year=prev_year, req_count=req_count, prog_count=prog_count,
                                     closed_count=closed_count)
            pdf = BytesIO()
            HTML(string=report).write_pdf(pdf)
            pdf.seek(0) 
            body = render_template('monthly_activity.html', name=customer.name, month=prev_month, year=prev_year, req=True)
            send_mail_with_pdf(recipient, subject, body, pdf=pdf)
            return 'Mail is sent'
        else:
            body = render_template('monthly_activity.html', name=customer.name, month=prev_month, year=prev_year, req=False)
            send_mail_with_pdf(recipient, subject, body)
            return 'Mail is sent'
