from celery.schedules import crontab
from flask import current_app as app
from application.celery.tasks import new_prof_checks, new_req_checks, send_monthly_report

celery_app = app.extensions['celery']

# sender.add_periodic_task(crontab(hour=18, minute=55), send_monthly_report.s(), name='Daily Reminder' )
# sender.add_periodic_task(crontab(minute=0, hour=0, day_of_month=1), send_monthly_report.s(), name='Send Monthly Activity Reports')
# sender.add_periodic_task(crontab(hour=18, minute=55, day_of_week='monday'), send_monthly_report.s(), name = 'Weekly Reminder' )

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        60.0,  
        new_prof_checks.s(),  
        name='Check New Professionals for Admin'
    )

    sender.add_periodic_task(
        60.0,  
        new_req_checks.s(),  
        name='Check Service Requests for Professionals'
    )

    sender.add_periodic_task(
        60.0,
        send_monthly_report.s(),
        name='Send Monthly Activity Reports'
    )