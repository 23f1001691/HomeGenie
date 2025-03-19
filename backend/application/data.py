from application.extensions import db, bcrypt
from application.models import User, Admin, Category

def initialize_data():
    existing_admin = User.query.filter_by(email='admin@gmail.com').first()
    if not existing_admin:
        new_user = User(email='admin@gmail.com', password=bcrypt.generate_password_hash('admin').decode('utf-8'),
                        role='admin')
        db.session.add(new_user)
        db.session.flush()  

        new_admin = Admin(user_id=new_user.id)
        db.session.add(new_admin)
        db.session.commit()

    categories = Category.query.all()
    
    if not categories:
        new_cat_1 = Category(name='AC & Appliance Repair', image_url='application/static/service/ac.jpg')
        db.session.add(new_cat_1)
        
        new_cat_2 = Category(name='Electrical', image_url='application/static/service/electrical.png')
        db.session.add(new_cat_2)
        
        new_cat_3 = Category(name='Plumbing & Carpentry', image_url='application/static/service/plumbing.png')
        db.session.add(new_cat_3)
        
        new_cat_4 = Category(name='Cleaning', image_url='application/static/service/cleaning.svg')
        db.session.add(new_cat_4)
        
        new_cat_5 = Category(name='Painting', image_url='application/static/service/painting.svg')
        db.session.add(new_cat_5)
        
        db.session.commit()
