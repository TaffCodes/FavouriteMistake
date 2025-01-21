from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserProfile, EmailLog

def notify_users(matches):
    for lost_item, found_item in matches:
        user = lost_item.user
        subject = 'Potential Match Found for Your Lost Item'
        html_content = render_to_string('email/match_notification.html', {
            'lost_item': lost_item,
            'found_item': found_item,
            'user': user,
        })
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, 'from@example.com', [user.email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        try:
            email.send()
            success = True
        except Exception as e:
            success = False
        
        # Log the email
        EmailLog.objects.create(
            user=user,
            subject=subject,
            body=html_content,
            success=success
        )