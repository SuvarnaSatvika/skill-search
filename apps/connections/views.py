from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Connection
from django.contrib.auth.models import User

@login_required
def send_request(request, to_user_id):
    from_user = request.user
    to_user = User.objects.get(id=to_user_id)
    if from_user != to_user and not Connection.objects.filter(from_user=from_user, to_user=to_user).exists():
        Connection.objects.create(from_user=from_user, to_user=to_user)
        messages.success(request, 'Connection request sent.')
    return redirect('search')

@login_required
def accept_request(request, request_id):
    conn = Connection.objects.get(id=request_id)
    if conn.to_user == request.user and conn.status == 'pending':
        conn.status = 'accepted'
        conn.save()
        messages.success(request, 'Connection accepted.')
    return redirect('connections_list')

@login_required
def reject_request(request, request_id):
    conn = Connection.objects.get(id=request_id)
    if conn.to_user == request.user and conn.status == 'pending':
        conn.status = 'rejected'
        conn.save()
        messages.success(request, 'Connection rejected.')
    return redirect('connections_list')

@login_required
def connections_list(request):
    received_pending = Connection.objects.filter(to_user=request.user, status='pending')
    accepted_conns = Connection.objects.filter(
        Q(from_user=request.user, status='accepted') | Q(to_user=request.user, status='accepted')
    )


    connected_users = set()
    for conn in accepted_conns:
        if conn.from_user == request.user:
            connected_users.add(conn.to_user)
        else:
            connected_users.add(conn.from_user)

    context = {
        'pending': received_pending,
        'accepted_users': connected_users,
    }
    return render(request, 'connections/list.html', context)