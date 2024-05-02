from django.shortcuts import render , redirect
from .models import Room,Message
from django.contrib import messages 
from django.contrib import messages as mg
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home import models
from django.utils import timezone
from django.contrib.sessions.models import Session

def get_active_users_count():
    # Get all non-expired session keys
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    
    # Extract user IDs from the session data
    user_ids = [s for s in active_sessions]
    
    # Count unique user IDs
    active_users_count = len(set(user_ids))
    
    return active_users_count




def rooms(request):
    rooms=Room.objects.all()


    # active_users_count = get_active_users_count()

    return render(request, "rooms.html",{"rooms":rooms})

def room(request,slug):
    if request.user.is_authenticated:
        room_name=Room.objects.get(slug=slug).name
        messages=Message.objects.filter(room=Room.objects.get(slug=slug))
        user_n=Room.objects.get(slug=slug).user
        print(user_n)
        
        return render(request, "room.html",{"room_name":room_name,"slug":slug,'messagess':messages ,'user_n':user_n})
    else:
        mg.warning(request, 'Please login first to join Chat Room')
        return redirect('/')


def logoutuser(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('/')


def deleteRoom(request ,slug):
    if request.user.is_authenticated:
        room=Room.objects.get(slug=slug)
        room.delete()
        messages.success(request, "Chat Room  has been deleted successfully")

    else:

        messages.error(request, "Permission denied, Only admin of this Room can delete this room.")
    
    return redirect('/')

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('loginusername')
        password = request.POST.get('loginPassword')
        
        user = authenticate(request, username=username, password=password)     
        
        if user is not None:
            
            login(request, user)
            messages.success(request , f"Welcome back  {request.user.get_full_name()}")
            return redirect('/')
        else:
            messages.error(request, 'Incorrect Username or Password')
            return redirect('/')

    messages.error(request, 'User does not exist')
    return redirect('/')



def createRoom(request):
    if request.method == 'POST'and request.user.is_authenticated:
        
        roomname = request.POST.get('roomname')
        tag = request.POST.get('tagname')
        rooms=Room.objects.filter(name=roomname)
        slugs=Room.objects.filter(slug=tag)
        if  not rooms and not slugs:
          
            user = request.user
            tag=tag.replace(" ","")
            if (len(roomname)==0 or len(tag)==0):
                messages.error(request , "Please fill all the  fields properly to create a new chat room. ")
            else:
                room=models.Room(name=roomname , slug=tag , user=user)
                room.save()
                messages.success(request , f"Your Chat Room has been created successfully...")
                return redirect(f'/')
        else:
             messages.error(request , "Chat Rooms with given room name or tag  is already exist.Choose different room name or tag for your ChatRoom")
    else:
        messages.warning(request, "Please Login first to create a new chat rooms.")
    return redirect('/')
        
       


def handleSignUp(request):
    if request.method=='POST':
         username=request.POST['username']
         fname=request.POST['fname']
         lname=request.POST['lname']
         email=request.POST['email']
         pass1=request.POST['pass1']
         pass2=request.POST['pass2']

         if (len(username) >10 ):
             messages.warning(request,"username must be under 10 character  ")
             return redirect('home')
      
         
         if pass1!=pass2:
             messages.warning(request, "Password didn't matched , try again....")
             return redirect('home')

         else:

         #create user
           try:
             myuser=User.objects.create_user(username , email , pass1)
             myuser.first_name=fname
             myuser.last_name=lname
             myuser.save()
             messages.success(request , "Your account has been created successfully....")
             return redirect('home')
           except:
               messages.error(request , "User already exist")
               return redirect('home')

    else:
        return HttpResponse("404- Not allowed")