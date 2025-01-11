from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, LostItemForm, FoundItemForm
from .models import LostItem, FoundItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from google.cloud import vision
from .matching import find_matches
import os
import json




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
    return render(request, 'home.html')

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

def report_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lost item reported successfully!')
            return redirect('hello_world')
    else:
        form = LostItemForm()
    return render(request, 'report_lost.html', {'form': form})


# Set up Google Cloud Vision client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './service-account-file.json'
client = vision.ImageAnnotatorClient()

def analyze_image(image_path):
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return ', '.join([f"{label.description} ({label.score:.2f})" for label in labels])

def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Found item reported successfully!')
            return redirect('hello_world')
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

def dashboard(request):
    matches = find_matches()
    print(f"Matches passed to template: {matches}")  # Debugging information
    return render(request, 'dashboard.html', {'matches': matches})
