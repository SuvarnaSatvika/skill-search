from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from .forms import MessageForm
from apps.connections.models import Connection
from django.contrib.auth.models import User

@login_required
def message_list(request, user_id):
    other_user = User.objects.get(id=user_id)

    if not Connection.objects.filter(
        Q(from_user=request.user, to_user=other_user, status='accepted') |
        Q(from_user=other_user, to_user=request.user, status='accepted')
    ).exists():
        return redirect('search')
    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('message_list', user_id=user_id)
    else:
        form = MessageForm()
    context = {
        'other_user': other_user,
        'chat_messages': chat_messages,
        'form': form,
    }
    return render(request, 'messaging/list.html', context)