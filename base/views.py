from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room,Topic
from .forms import RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
# rooms=[
#     {'id':1,'name':'Lets learn python','topic':'Python','description':'This is a python study room'},
#     {'id':2,'name':'Lets learn django','topic':'Django','description':'This is a django study room'},
#     {'id':3,'name':'Lets learn java','topic':'Java','description':'This is a java study room'},
#     {'id':4,'name':'Lets learn c++','topic':'C++','description':'This is a c++ study room'},
#     {'id':5,'name':'Lets learn c#','topic':'C#','description':'This is a c# study room'},
#     {'id':6,'name':'Lets learn javascript','topic':'Javascript','description':'This is a javascript study room'},
#     {'id':7,'name':'Lets learn html','topic':'Html','description':'This is a html study room'},
#     {'id':8,'name':'Lets learn css','topic':'Css','description':'This is a css study room'},
#     {'id':9,'name':'Lets learn react','topic':'React','description':'This is a react study room'},
#     {'id':10,'name':'Lets learn angular','topic':'Angular','description':'This is a angular study room'},
#     {'id':11,'name':'Lets learn vue','topic':'Vue','description':'This is a vue study room'},
#     {'id':12,'name':'Lets learn php','topic':'Php','description':'This is a php study room'},
#     {'id':13,'name':'Lets learn laravel','topic':'Laravel','description':'This is a laravel study room'},

# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
     username=request.POST.get('username').lower()
     password=request.POST.get('password')

     try:
         user=User.objects.get(username=username)
        
     except:
            messages.error(request,'Username does not exist')
        
        
     user=authenticate(request,username=username,password=password)
     if user is not None:
            login(request,user)
            return redirect('home')
     else:
            messages.error(request,'Username or password is incorrect')

    context={'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request,'An error occured during registration')



    return render(request,'base/login_register.html',{'form':form})


def home(request):
    q= request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )

    topics=Topic.objects.all()
    room_count=rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request, 'base/home.html',context)


def room(request ,pk):
   room=Room.objects.get(id=pk)
   context={'room':room}
    
   return render(request,"base/room.html" ,context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
 
    return render(request,"base/room_form.html",context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('You are not alowed here !!!')
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,"base/room_form.html",context)
@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('You are not alowed here !!!')



    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,"base/delete.html",{'obj':'room'})
