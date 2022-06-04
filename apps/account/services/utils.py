from django.core.mail import send_mail


def send_activate_code(activate_code, email: str):
    title = 'Hello, it is a link for activating your acc'
    message = f'Please click the link to activate your acc http://127.0.0.1:8000/account/activate/{activate_code}/'
    sender = 'SnakeShop@test.com'

    send_mail(
        title,
        message,
        sender,
        [email],
        fail_silently=False,
    )


def send_new_password(email: str, new_password):
    title = 'Hello, it is a link for resetting your acc on'
    message = f'This is a new password for your acc {new_password}'
    sender = 'SnakeShop@test.com'

    send_mail(
        title,
        message,
        sender,
        [email],
        fail_silently=False,
    )