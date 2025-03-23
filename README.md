# HomeGenie
A platform that provides home servicing solutions by connecting service professionals with customers, managed by an admin, featuring a clear UI and a robust backend.

# LOGOUT did not remove token from cookies. It just reassigns on subsequent login.
# Add JWT req and Role req for needed APIs
# Logout and go to homepage for 404 Page
# While adding service, add category id
# @jwt_required doesnot work since token is not added in cookies
# Admin should get a daily reminder to check new professionals
# Professional should get a mail once they are approved or rejected
# Check put method in prof api. Approval. Rejection.
# After delete service, it dont automatically take it away from display. Reload is needed as of now
# While changing, service name in EDIT, service name unique constraint failed
# Changging second service, changes the value of first one
# After admin approval  also, it is not re-rendering automatically like delete but it reloads for reject approval
# Professional rating is shown as 0 in customer dash if its a new professional or the prof who doesnot get any rating
# Snippet - props.disabled checks for form validation
# For new professional, if no request is sent. His dash will be empty. DO something for that. For customer req page also. And prof history page also.
# jwt get_jwt issue
# "props.disabled" or false (SubmitBtn) in SNIPPET
# Login form and registration form frontend validation
# Customer Req also after cancel req, we need to reload