import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def get_default_user():
    default_user, created = User.objects.get_or_create(username='defaultuser', defaults={'password': 'defaultpassword'})
    return default_user.id
User = get_user_model()

class LostItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)  # Set UUID as primary key
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='lost_items/')
    reported_at = models.DateTimeField(auto_now_add=True)
    vision_labels = models.TextField(blank=True, null=True)  # Store Vision API labels


    def __str__(self):
        return f"RL-{str(self.uuid)[:4]}"

class FoundItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)  # Set UUID as primary key
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='found_items/')
    reported_at = models.DateTimeField(auto_now_add=True)
    vision_labels = models.TextField(blank=True, null=True)  # Store Vision API labels


    def __str__(self):
        return f"RF-{str(self.uuid)[:4]}"
    
class ItemMatch(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE)
    match_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Match: {self.lost_item} - {self.found_item} ({self.get_status_display()})"
    
    class Meta:
        unique_together = ('lost_item', 'found_item')

class EmailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Email to {self.user.email} - {self.subject}"