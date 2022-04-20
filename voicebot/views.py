from django.shortcuts import render

def index(request):
    return render(request, 'voicebot/index.html')

def room(request, room_name):
    return render(request, 'voicebot/room.html', {
        'room_name': room_name
    })