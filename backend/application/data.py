from application.extensions import db, bcrypt
from application.models import User, Admin

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

