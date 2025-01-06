from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm, LostItemForm, FoundItemForm
from .models import LostItem, FoundItem
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate



class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@api_view(['GET'])
def hello_world_api(request):
    return Response({"message": "Welcome to the Smart Lost and Found Platform"})


@login_required
def hello_world(request):
    return render(request, 'hello_world.html')

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
            return redirect('home')
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
            return redirect('home')
    else:
        form = LostItemForm()
    return render(request, 'report_lost.html', {'form': form})

def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FoundItemForm()
    return render(request, 'report_found.html', {'form': form})

def item_details(request, id):
    lost_item = get_object_or_404(LostItem, id=id)
    found_item = get_object_or_404(FoundItem, id=id)
    return render(request, 'item_details.html', {'lost_item': lost_item, 'found_item': found_item})