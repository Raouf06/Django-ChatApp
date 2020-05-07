from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import Message,Chat
from django.http import HttpResponse

def index(request):
	return render(request, 'index.html')
    
@login_required
def room(request, room_name):
	if User.objects.filter(username=room_name).first():
		if not User.objects.filter(username=room_name).first() == request.user:
			second = User.objects.get(username=room_name)
			if not Chat.objects.filter(users=request.user).filter(users=second).first():
				instance = Chat.objects.create(chat_id=request.user.username + second.username)
				instance.users.add(request.user)
				instance.users.add(second)
				lol = Chat.objects.filter(users=request.user).filter(users=second).first()
			else:
				lol = Chat.objects.filter(users=request.user).filter(users=second).first()
			return render(request, 'room.html', {
				'room_name_json': mark_safe(json.dumps(room_name)),
				'username':  mark_safe(json.dumps(request.user.username)),
				'receiver': room_name,
				'chat': lol.chat_id,
			})
		else:
			return HttpResponse("<center><h2>You can't start a convo with yourself</h2></center>")
	else:
		return HttpResponse('<center><h2>No user with that name</h2></center>')