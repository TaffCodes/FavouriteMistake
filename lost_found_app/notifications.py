from django.core.mail import send_mail
from .models import UserProfile

def notify_users(matches):
    for lost_item, found_item in matches:
        user = lost_item.userprofile.user
        send_mail(
            'Potential Match Found for Your Lost Item',
            f'We found a potential match for your lost item "{lost_item.name}". '
            f'Please check the found item "{found_item.name}" at {found_item.location}.',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )