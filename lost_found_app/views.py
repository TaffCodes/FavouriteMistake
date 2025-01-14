from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import LostItemForm, FoundItemForm, LostIDCardForm, FoundIDCardForm
from .models import LostItem, FoundItem, LostIDCard, FoundIDCard
from .matching import find_matches
from google.cloud import vision
import os

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

def report_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.vision_labels = analyze_image(lost_item.image.path)
            lost_item.save()
            messages.success(request, 'Lost item reported successfully!')
            return redirect('hello_world')
    else:
        form = LostItemForm()
    return render(request, 'report_lost.html', {'form': form})

def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            found_item = form.save(commit=False)
            found_item.vision_labels = analyze_image(found_item.image.path)
            found_item.save()
            messages.success(request, 'Found item reported successfully!')
            return redirect('hello_world')
    else:
        form = FoundItemForm()
    return render(request, 'report_found.html', {'form': form})

def report_lost_id(request):
    if request.method == 'POST':
        form = LostIDCardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lost ID card reported successfully!')
            return redirect('hello_world')
    else:
        form = LostIDCardForm()
    return render(request, 'report_lost_id.html', {'form': form})

def report_found_id(request):
    if request.method == 'POST':
        form = FoundIDCardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Found ID card reported successfully!')
            return redirect('hello_world')
    else:
        form = FoundIDCardForm()
    return render(request, 'report_found_id.html', {'form': form})

def search_id(request):
    query = request.GET.get('q')
    lost_ids = LostIDCard.objects.filter(id_number=query)
    found_ids = FoundIDCard.objects.filter(id_number=(query))
    return render(request, 'search_results.html', {'lost_ids': lost_ids, 'found_ids': found_ids})

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