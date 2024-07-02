from django.core.mail import send_mail

class Emailer:
    @staticmethod
    def send_email_after_account_creation(email, password):

        send_mail(
            "Account Created",
            f"Your account has been created. Your password is {password}",
            "kunoomaking@gmail.com",
            [email],
            fail_silently=True
        )
    