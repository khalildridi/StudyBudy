from multiprocessing import context
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .models import Room, Message
from .forms import RoomForm 
# Create your views here.

def home(request):
    rooms=Room.objects.all()
    context={'rooms':rooms}

    return render(request,'base/home.html',context)


def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    context= { 'room':room, 'room_messages':room_messages }
    if request.method == 'POST':
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    return render(request,'base/room.html',context)


def createRoom(request):
    form=RoomForm()

    if request.method =='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete() 
        return redirect('home')
        
    return render(request,'base/delete.html',{'obj':room})

