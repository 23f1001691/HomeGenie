from flask_restful import Resource
from application.extensions import api, db, cache
from application.models import Professional, User, Service, ServiceRequest, Payment, Customer, Category
from flask import url_for
import os
from datetime import datetime
from application.utils import role_required
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from sqlalchemy.orm import aliased

class AdminDashAPI(Resource):
    @jwt_required()
    @role_required(['admin'])
    @cache.cached(timeout = 60, key_prefix='admin_dashboard')
    def get(self):
        active_customers = int(db.session.query(func.count(User.id)) 
            .join(Customer, Customer.user_id == User.id) 
            .filter(Customer.flag == False)  
            .scalar() or 0) 
        active_professionals = int(db.session.query(func.count(User.id)) 
            .join(Professional, Professional.user_id == User.id) 
            .filter(Professional.flag == False, Professional.status == 'Approved')  
            .scalar() or 0) 
        active_users = active_customers + active_professionals
        total_bookings = int(db.session.query(func.count(ServiceRequest.id))
                            .filter(ServiceRequest.status.in_(['Assigned', 'Paid', 'Closed'])) 
                            .scalar() or 0)
        running_services = int(db.session.query(func.count(Service.id)).scalar() or 0)
        revenue = db.session.query(func.sum(Payment.amount)).scalar() or 0
        rev_data = get_revenue_by_services()
        req_data = get_request_count()

        return {
            "active_users": active_users,
            "total_bookings": total_bookings,
            "revenue": revenue,
            "running_services":  running_services,
            "rev_data": rev_data,
            "req_data": req_data
        }, 200

api.add_resource(AdminDashAPI, '/admin-dash')


def get_revenue_by_services():
    service_alias = aliased(Service)

    revenue_data = (
        db.session.query(
            Category.name.label('service'),
            func.coalesce(func.sum(Payment.amount), 0).label('revenue')
        )
        .join(service_alias, service_alias.category_id == Category.id, isouter=True)
        .join(ServiceRequest, ServiceRequest.service_id == service_alias.id, isouter=True)
        .join(Payment, Payment.service_request_id == ServiceRequest.id, isouter=True)
        .group_by(Category.name)
        .order_by(func.sum(Payment.amount).desc()) 
        .limit(10) 
        .all()
    )  

    result = {}
    labels = []
    values = []
    for row in revenue_data:
        labels.append(row.service)
        values.append(float(row.revenue) if row.revenue else 0.0  )
    result["labels"]=labels
    result["values"]=values

    return result

def get_request_count():
    requested = int(db.session.query(func.count(ServiceRequest.id)).filter(
            ServiceRequest.status == 'Requested').scalar() or 0)
    rejected = int(db.session.query(func.count(ServiceRequest.id)).filter(
                ServiceRequest.status == 'Rejected').scalar() or 0)
    assigned = int(db.session.query(func.count(ServiceRequest.id)).filter(
                ServiceRequest.status == 'Assigned').scalar() or 0)
    closed = int(db.session.query(func.count(ServiceRequest.id)).filter(
                ServiceRequest.status.in_(['Paid', 'Closed'])).scalar() or 0)

    return [requested, assigned, rejected, closed]

        










