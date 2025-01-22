from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailLog
from django.conf import settings
import mimetypes

def notify_users(matches):
    for lost_item, found_item in matches:
        user = lost_item.user
        subject = 'Potential Match Found for Your Lost Item'
        html_content = render_to_string('email/match_notification.html', {
            'lost_item': lost_item,
            'found_item': found_item,
            'user': user,
            'base_url': settings.BASE_URL,
        })
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, 'from@example.com', [user.email])
        email.attach_alternative(html_content, "text/html")
        
        # Attach lost item image
        if lost_item.image:
            lost_item_image_path = lost_item.image.path
            lost_item_image_name = lost_item.image.name
            lost_item_image_mime_type, _ = mimetypes.guess_type(lost_item_image_path)
            with open(lost_item_image_path, 'rb') as img:
                email.attach(lost_item_image_name, img.read(), lost_item_image_mime_type)
            email.attach_alternative(html_content.replace(
                '{{ lost_item.image.url }}', f'cid:{lost_item_image_name}'), "text/html")
        
        # Attach found item image
        if found_item.image:
            found_item_image_path = found_item.image.path
            found_item_image_name = found_item.image.name
            found_item_image_mime_type, _ = mimetypes.guess_type(found_item_image_path)
            with open(found_item_image_path, 'rb') as img:
                email.attach(found_item_image_name, img.read(), found_item_image_mime_type)
            email.attach_alternative(html_content.replace(
                '{{ found_item.image.url }}', f'cid:{found_item_image_name}'), "text/html")
        
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