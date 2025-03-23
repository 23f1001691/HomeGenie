from flask_restful import Resource
from flask import request
import os
from datetime import datetime
from dotenv import load_dotenv
import razorpay
from flask_jwt_extended import jwt_required
from application.utils import role_required
from application.extensions import db, api
from application.models import ServiceRequest, Payment
from flask_cors import cross_origin

load_dotenv()
razorpay_client = razorpay.Client(auth=(os.getenv('RAZORPAY_CLIENT_ID'), os.getenv('RAZORPAY_ACCESS_KEY')))

class PaymentAPI(Resource):
    @jwt_required()
    @role_required(['customer'])
    @cross_origin()
    def get(self, service_request_id):
        service_request = ServiceRequest.query.get(service_request_id)
        if not service_request_id:
            return {'message': 'Service Request ID is required'}, 400
        amount = (service_request.service.base_price)*100
        currency = 'INR'
        order_data = {
            'amount': amount,
            'currency': currency,
            'payment_capture': '1'
        }
        add_on = {
            'key': os.getenv('RAZORPAY_CLIENT_ID'), 
            'id':service_request.id
        }
        order = razorpay_client.order.create(data=order_data)
        return {'order': order, 'add_on': add_on}, 200
    
    @jwt_required()
    @role_required(['customer'])
    @cross_origin()
    def post(self):
        data = request.json
        required_fields = ['service_request_id', 'payment_id', 'order_id', 'signature']
        for field in required_fields:
            if not data.get(field):
                return f"{field} is required!", 400
        try:
            service_request_id = data['service_request_id']
            payment_id = data['payment_id']
            order_id = data['order_id']
            signature = data['signature']
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)
            payment = razorpay_client.payment.fetch(payment_id)
            if payment['status'] == 'captured':
                service_request = ServiceRequest.query.get(service_request_id)
                service_request.status = 'Paid'
                service_request.date_of_completion = datetime.now().date()
                amount = service_request.service.base_price
                payment_date = datetime.now()
                new_transaction = Payment(amount=amount, payment_date=payment_date, service_request_id=service_request_id)
                db.session.add(new_transaction)
                db.session.commit()
                return {'message': 'Payment successful!'}, 200
            else:
                return {'message': 'Payment not successful.'}, 400
        except:
            return {'message': 'Something went wrong!'}, 500
        
api.add_resource(PaymentAPI, '/payment/<int:service_request_id>', '/payment')

