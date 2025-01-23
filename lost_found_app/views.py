from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, LostItemForm, FoundItemForm
from .models import LostItem, FoundItem, ItemMatch
from .matching import find_matches_for_item
import os
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from google.cloud import vision
import time
from google.api_core.exceptions import ServiceUnavailable
from .notifications import notify_users





class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@api_view(['GET'])
def hello_world_api(request):
    return Response({"message": "Welcome to the Smart Lost and Found Platform"})


@login_required
def hello_world(request):
    lost_items = LostItem.objects.all()
    found_items = FoundItem.objects.all()
    return render(request, 'hello_world.html', {'lost_items': lost_items, 'found_items': found_items})

def home(request):
    matches = ItemMatch.objects.all().order_by('-created_at')[:9]
    return render(request, 'home.html', {'matches': matches})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
            
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})



# Set up Google Cloud Vision client
SERVICE_KEY = config('SERVICE_KEY')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_KEY
client = vision.ImageAnnotatorClient()

def analyze_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    
    retries = 3
    for attempt in range(retries):
        try:
            response = client.label_detection(image=image)
            labels = response.label_annotations
            if not labels:
                return ''
            return ', '.join([f"{label.description} ({label.score:.2f})" for label in labels])
        except ServiceUnavailable as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e

@login_required
def report_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.user = request.user
            lost_item.save()
            # Analyze image with Vision API
            lost_item.vision_labels = analyze_image(lost_item.image.path)
            lost_item.save()
            
            # Run matching algorithm
            matches = find_matches_for_item(lost_item)
            notify_users(matches)

            messages.success(request, 'Lost item reported successfully!')
            return redirect('dashboard')
    else:
        form = LostItemForm()
    return render(request, 'report_lost.html', {'form': form})

@login_required
def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.user = request.user
            found_item.save()
            # Analyze image with Vision API 
            found_item.vision_labels = analyze_image(found_item.image.path)
            found_item.save()
            
            # Run matching algorithm
            matches = find_matches_for_item(found_item, is_found=True)
            if matches:
                notify_users(matches)

            messages.success(request, 'Found item reported successfully!')
            return redirect('dashboard')
    else:
        form = FoundItemForm()
    return render(request, 'report_found.html', {'form': form})

def item_details(request, id):
    try:
        lost_item = LostItem.objects.get(uuid=id)
        found_item = None
    except LostItem.DoesNotExist:
        lost_item = None
        found_item = get_object_or_404(FoundItem, uuid=id)
    return render(request, 'item_details.html', {'lost_item': lost_item, 'found_item': found_item})


@login_required
def dashboard(request):
    matches = ItemMatch.objects.all().order_by('-created_at')
    for match in matches:
        if match.match_score > 0.6:
            match.level = 'High match'
        elif match.match_score > 0.2:
            match.level = 'Medium match'
        else:
            match.level = 'Low match'
    return render(request, 'dashboard.html', {'matches': matches})

