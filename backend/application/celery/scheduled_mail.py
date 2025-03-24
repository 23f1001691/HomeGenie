from flask_mail import Message
from application.extensions import mail
from flask import current_app

def send_mail(recipient, subject, body, is_html=False):
    sender = (current_app.config['MAIL_NAME'], current_app.config['MAIL_USERNAME'])
    msg = Message(subject, sender=sender, recipients=[recipient])

    if is_html:
        msg.html = body
    else:
        msg.body = body

    try:
        mail.send(msg)
        return {"message": "Email is sent successfully"}, 200
    except Exception as e:
        return {"message": e}, 500

def send_mail_with_pdf(recipient, subject, body, pdf=False):
    sender = (current_app.config['MAIL_NAME'], current_app.config['MAIL_USERNAME'])
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.html = body

    if pdf:
        msg.attach("monthly_report.pdf", "application/pdf", pdf.read())

    try:
        mail.send(msg)
        return {"message": "Report is sent successfully"}, 200
    except Exception as e:
        return {"message": e}, 500


