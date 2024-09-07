from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from utils import EmailException
from django.conf import settings


def send_mail_using_smtp(email_data):
    try:
        connection = get_connection(
            backend=settings.EMAIL_BACKEND,
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=True,
        )
        send_mail(
            subject=email_data.get("subject"),
            message="",
            html_message=email_data.get("message"),
            from_email=email_data.get("from"),
            recipient_list=email_data.get("recipient"),
            connection=connection,
            fail_silently=False,
        )
    except Exception as exc:
        print("Exception:", str(EmailException(exc)))
        pass


def get_mail_template(key, data):
    templates = {
        "reset": f"<h3>Click on this <a href={data.get('reset_link')}>Link</a> to reset password </h3>",
        "login_credentials": render_to_string("invitation_template.html", context=data),
    }
    return templates[key]
