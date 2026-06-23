from flask import Flask, current_app
from flask_mail import Mail, Message

# Create the mail extension instance globally (unattached)
mail = Mail()

def init_mail(app: Flask):
    """
    Initialize Flask-Mail with the app configuration.
    This connects the MAIL_ keys from Config to the extension.
    """
    mail.init_app(app)


def send_email(subject, body=None, to_email=None, html=None, template_path=None, context=None):
    """
    Send an email using Flask-Mail.
    It automatically reads configurations from the active application context.
    """
    try:
        env = current_app.config.get('PYTHON_ENV', 'dev')
        if env != 'dev':
            print("Email sending suppressed in non-dev environment.")
            return True

        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body
        )
        
        # If your route passes a rendered HTML template string, use it
        if html:
            msg.html = html
        # If your route passes a template path and context, we can render it here too
        elif template_path and context:
            from flask import render_template
            msg.html = render_template(template_path, **context)

        mail.send(msg)
        print("Email sent successfully!")
        return True

    except Exception as e:
        print("Email error:", e)
        return False


# =====================================================================
# For Local Testing Only: Running this file directly
# =====================================================================
if __name__ == "__main__":
    from config import Config
    
    # Create a temporary test app and load your central configuration
    test_app = Flask(__name__)
    test_app.config.from_object(Config)
    
    # Initialize the mail setup
    init_mail(test_app)
    
    # Run inside the application context spotlight
    with test_app.app_context():
        send_email(
            subject="Testing Centralized Flask-Mail",
            body="It works! No more duplicate configurations.",
            to_email="adeyemiemmanuel547@gmail.com"
        )