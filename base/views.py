from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import models
from . import forms

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = models.Topic.objects.all()[0:5]
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q) |
        Q(description__icontains=q))
    
    room_count = rooms.count()
    room_messages = models.Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    
    return render(request, 'home.html', context)

def room(request, pk):
    room = models.Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = models.Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    
    return render(request, 'room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = models.Topic.objects.all()
    
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    page = 'create'
    topics = models.Topic.objects.all()
    form = forms.RoomForm()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)
        
        models.Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )       
            
    context = {'form': form, 'topics': topics, 'page': page}
    
    return render(request, 'create_room.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    page = 'update'
    room = models.Room.objects.get(id=pk)
    form = forms.RoomForm(instance=room)
    topics = models.Topic.objects.all()

    
    if request.user != room.host:
        return HttpResponse('You cannot perfom this action')
    
    elif request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = models.Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        
        room.save()
        
        return redirect('home')
        
    context = {'form': form, 'topics': topics, 'room': room, 'page': page}
    return render(request, 'create_room.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = models.Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You cannot perfom this action')
    
    elif request.method == 'POST':
        room.delete()
        return redirect('home')
        
    context = {'obj': room}
    return render(request, 'delete.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'No user found. Please check username')
            
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')
    
def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong. The username must already be taken. Try a different username')
            return redirect('register')
            
    
    context = {'page': page, 'form': form}
    return render(request, 'register.html', context)

@login_required(login_url='login')
def deleteComment(request, pk):
    comment = models.Message.objects.get(id=pk)
    
    if request.user != comment.user:
        HttpResponse('Not allowed')
        
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj': comment})

@login_required(login_url='login')
def updateComment(request, pk):
    comment = models.Message.objects.get(id=pk)
    
    if request.user != comment.user:
        HttpResponse('Not allowed')
        
    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.save()
        
        return redirect('home')
    
    return render(request, 'room.html', {'obj': room})

@login_required(login_url='login')
def updateUser (request):
    user = request.user
    form = forms.UserForm(instance=user)
    
    if request.method == 'POST':
        form = forms.UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
        else:
            messages.error(request, 'Something went wrong. The username must already be taken. Try a different username')
            return redirect('update-user')
        
        return redirect('profile', pk=user.id)
    
    context = {'form': form}
    return render(request, 'update_user.html', context)

def topics (request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = models.Topic.objects.filter(name__icontains=q)
    
    context = {'topics': topics}
    return render(request, 'topics.html', context)

def activities (request):
    room_messages = models.Message.objects.all()
    
    context = {'room_messages': room_messages}
    return render(request, 'activity.html', context)