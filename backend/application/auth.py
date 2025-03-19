from flask import jsonify, request
from application.models import User
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from application.extensions import bcrypt, db
from flask import current_app as app

@app.post('/auth/login')
def login():
    
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not email:
        return jsonify({"message":"Email not provided"}), 400
    if not password:
        return jsonify({"message":"Password not provided"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message":"User does not exist"}), 404
    if not (bcrypt.check_password_hash(user.password, password)):
        return jsonify({"message":"Incorrect password"}), 400
    
    if user.professional:
        if user.professional.flag == True:
            return jsonify({"message":"Professional is flagged by admin. So could not login."}), 400
        if user.professional.status == 'Unapproved':
            return jsonify({"message":"Professional is not approved by admin. So could not login."}), 400
        
    if user.customer:
        if user.customer.flag == True:
            return jsonify({"message":"Customer is flagged by admin. So could not login."}), 400
    
    is_first_session = False
    if user.is_first_session:  
        is_first_session = True
        #Check alternate way to change this field once the user details is updated after the first login
        user.is_first_session = False 
        db.session.commit()  

    access_token = create_access_token(identity=user.id)

    response = jsonify(
        {
            "access_token":access_token,
            "message":"Login Successful",
            "role":user.role,
            "user_id":user.id,
            "is_first_session":is_first_session
        }
    )

    set_access_cookies(response, access_token)

    return response.get_json(), 200

@app.post('/auth/logout')
def logout():
    response = jsonify({"message": "Logged out successfully."})
    unset_jwt_cookies(response)
    return response, 200


