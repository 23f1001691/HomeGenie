from application.extensions import db, bcrypt
from datetime import datetime
from datetime import date
from sqlalchemy import event

class User(db.Model):
    __tablename__ = 'user'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  
    is_first_session = db.Column(db.Boolean, default=True)
    is_profile_completed = db.Column(db.Boolean, default=False)

    #Relationships
    admin = db.relationship('Admin', uselist=False, cascade="all,delete,save-update", backref='user')
    customer = db.relationship('Customer', uselist=False, cascade="all,delete,save-update", backref='user')
    professional = db.relationship('Professional', uselist=False, cascade="all,delete,save-update", backref='user')

    def __repr__(self):
        return f'<User {self.email}>'
    
class Admin(db.Model):
    __tablename__ = 'admin'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Admin {self.user.email}>'

class Customer(db.Model):
    __tablename__ = 'customer'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=False)  
    flag = db.Column(db.Boolean, nullable=True, default=False)

    #Relationships
    service_requests = db.relationship('ServiceRequest',cascade="all,delete",backref="customer")

    def __repr__(self):
        return f'<Customer {self.user.email}>'

@event.listens_for(Customer, 'before_insert')
def set_default_customer_profile(mapper, connection, target):
    if not target.profile_pic:  
        target.profile_pic = 'application/static/profile/default.jpeg'

class Professional(db.Model):
    __tablename__ = 'professional'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(100), nullable=True)    
    contact_no = db.Column(db.Integer, nullable=True)            
    experience = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String, nullable=True)
    resume = db.Column(db.String(255), nullable=False)  
    created_date = db.Column(db.Date, nullable=False, default=date.today)
    profile_pic = db.Column(db.String(255), nullable=False)  
    address = db.Column(db.String(255), nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default='Unapproved')
    rating = db.Column(db.Float, nullable=False, default=0.0)
    flag = db.Column(db.Boolean, nullable=True, default=False)

    #Relationships
    service_requests = db.relationship('ServiceRequest',cascade="all,delete",backref="professional")

    # Temporarily store category name
    category = db.Column(db.String(100), nullable=True) 

    def __repr__(self):
        return f'<Professional {self.user.email}>'

@event.listens_for(Professional, 'before_insert')
def set_default_prof_profile(mapper, connection, target):
    if not target.profile_pic:  
        target.profile_pic = 'application/static/profile/default.jpeg'

class Category(db.Model):
    __tablename__ = 'category'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    image_url = db.Column(db.String(255), nullable=False)

    #Relationships
    services = db.relationship('Service', backref='category', lazy=True)

class Service(db.Model):
    __tablename__ = 'service'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    base_price = db.Column(db.Float,  nullable=False)
    time_req = db.Column(db.Float,  nullable=False)
    
    #Relationships
    professionals = db.relationship('Professional',cascade="all,delete",backref="service")
    service_requests = db.relationship('ServiceRequest',cascade="all,delete",backref="service")

class ServiceRequest(db.Model):
    __tablename__ = 'service_request'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    date_of_request = db.Column(db.Date, nullable=False, default=date.today)
    date_of_completion = db.Column(db.Date, nullable=True)
    status_updated_by = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='Requested')

    #Relationships
    review = db.relationship('Review', back_populates='service_request', uselist=False, cascade="all,delete")
    payment = db.relationship('Payment', back_populates='service_request', uselist=False, cascade="all,delete")

class Review(db.Model):
    __tablename__ = 'review'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    feedback = db.Column(db.String,  nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    
    #Relationships
    service_request = db.relationship('ServiceRequest', back_populates='review')

class Payment(db.Model):
    __tablename__ = 'payment'

    #Fields
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_request.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    
    #Relationships
    service_request = db.relationship('ServiceRequest', back_populates='payment')
