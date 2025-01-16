import uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LostItem(models.Model):
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
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE)
    found_item = models.ForeignKey(FoundItem, on_delete=models.CASCADE)
    match_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('lost_item', 'found_item')
    
# class LostIDCard(models.Model):
#     id_number = models.CharField(max_length=20, unique=True)
#     first_name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     reported_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.id_number

# class FoundIDCard(models.Model):
#     id_number = models.CharField(max_length=20, unique=True)
#     first_name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     reported_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.id_number