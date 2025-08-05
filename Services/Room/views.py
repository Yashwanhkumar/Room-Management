from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Allservices, ServiceRecord, Room
from django.db.models import Sum, Count, Q
from django.contrib import messages
from datetime import datetime


# --- Main Application Views ---

@login_required
def services_dashboard(request):
    user_rooms = request.user.rooms.all()
    if user_rooms.exists():
        first_room = user_rooms.first()
        return redirect('room_dashboard', room_id=first_room.id)
    else:
        context = {'user_rooms': user_rooms}
        return render(request, "Room/home.html", context)


@login_required
def room_dashboard_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user not in room.members.all():
        return redirect('services_dashboard')

    if request.method == "POST":
        service_name = request.POST.get("serviceName")
        service_description = request.POST.get("description")
        if service_name and service_description:
            Allservices.objects.create(
                room=room,
                created_by=request.user,
                service_name=service_name,
                description=service_description
            )
            return redirect('room_dashboard', room_id=room.id)

    room_services = room.services.all().order_by('-id')
    context = {
        'room': room,
        'services': room_services,
        'is_owner': request.user == room.owner
    }
    return render(request, 'Room/room_dashboard.html', context)


# --- Service Management Views ---

@login_required
def manage_service(request, service_id):
    service = get_object_or_404(Allservices, pk=service_id)

    # Security check: only members of the room can view this page
    if request.user not in service.room.members.all():
        return redirect('services_dashboard')

    if request.method == 'POST':
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        if description and cost:
            ServiceRecord.objects.create(
                service=service,
                description=description,
                cost=cost
            )
            return redirect('manage_service', service_id=service.id)

    service_records = service.records.all().order_by('-created_at')

    # --- Add this logic to check for ownership ---
    is_owner = request.user == service.room.owner

    context = {
        'service': service,
        'service_records': service_records,
        'is_owner': is_owner  # Pass the ownership status to the template
    }
    return render(request, 'Room/manage_service.html', context)

@login_required
def edit_service_record(request, record_id):
    record = get_object_or_404(ServiceRecord, pk=record_id)
    # Allow staff to edit any record
    if not request.user.is_staff and request.user not in record.service.room.members.all():
        return redirect('services_dashboard')

    if request.method == 'POST':
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        if description and cost:
            record.description = description
            record.cost = cost
            record.save()
            # Redirect back to the admin dashboard if the user is staff
            if request.user.is_staff:
                return redirect('admin_dashboard')
            return redirect('manage_service', service_id=record.service.id)
    context = {'record': record}
    return render(request, 'Room/edit_record.html', context)


@login_required
def delete_service_record(request, record_id):
    record = get_object_or_404(ServiceRecord, pk=record_id)
    # Allow staff to delete any record
    if not request.user.is_staff and request.user not in record.service.room.members.all():
        return redirect('services_dashboard')

    if request.method == 'POST':
        service_id = record.service.id
        record.delete()
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('manage_service', service_id=service_id)
    return redirect('services_dashboard')


# --- Room Management Views ---

@login_required
def room_list_view(request):
    user_rooms = request.user.rooms.all()
    return render(request, 'Room/room_list.html', {'rooms': user_rooms})


@login_required
def create_room_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            room = Room.objects.create(name=name, description=description, owner=request.user)
            room.members.add(request.user)
            return redirect('room_list')
    return render(request, 'Room/create_room.html')


@login_required
def join_room_view(request):
    if request.method == 'POST':
        invite_code = request.POST.get('invite_code', '').upper()
        try:
            room_to_join = Room.objects.get(invite_code=invite_code)
            room_to_join.members.add(request.user)
            messages.success(request, f"You have successfully joined the room: {room_to_join.name}")
            return redirect('room_list')
        except Room.DoesNotExist:
            messages.error(request, "Invalid invite code. Please try again.")
    return render(request, 'Room/join_room.html')


@login_required
def room_detail_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user not in room.members.all():
        messages.error(request, "You are not a member of this room.")
        return redirect('room_list')
    context = {'room': room, 'is_owner': request.user == room.owner}
    return render(request, 'Room/room_detail.html', context)


# --- Owner and Admin Dashboards ---

@login_required
def room_owner_dashboard_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user != room.owner:
        return redirect('room_dashboard', room_id=room.id)
    now = datetime.now()
    monthly_expenses = ServiceRecord.objects.filter(
        service__room=room, created_at__year=now.year, created_at__month=now.month
    ).aggregate(total=Sum('cost'))['total'] or 0
    all_records = ServiceRecord.objects.filter(service__room=room).order_by('-created_at')
    context = {
        'room': room,
        'monthly_expenses': monthly_expenses,
        'all_records': all_records,
        'current_month': now.strftime('%B %Y')
    }
    return render(request, 'Room/room_owner_dashboard.html', context)


def is_staff_member(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff_member)
def admin_dashboard_view(request):
    all_records = ServiceRecord.objects.select_related('service__room', 'service__created_by').all()

    search_query = request.GET.get('q', '')
    service_filter = request.GET.get('service', '')
    date_filter = request.GET.get('date', '')

    if search_query:
        all_records = all_records.filter(
            Q(service__service_name__icontains=search_query) |
            Q(service__created_by__username__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if service_filter:
        all_records = all_records.filter(service__service_name=service_filter)

    if date_filter:
        all_records = all_records.filter(created_at__date=date_filter)

    total_users = User.objects.count()
    total_records = all_records.count()
    total_costs = all_records.aggregate(total=Sum('cost'))['total'] or 0

    most_used_service_query = all_records.values('service__service_name').annotate(count=Count('service')).order_by(
        '-count').first()
    most_used_service = most_used_service_query['service__service_name'] if most_used_service_query else "N/A"

    distinct_services = Allservices.objects.values_list('service_name', flat=True).distinct()

    context = {
        'total_users': total_users,
        'total_records': total_records,
        'total_costs': total_costs,
        'most_used_service': most_used_service,
        'all_records': all_records.order_by('-created_at'),
        'distinct_services': distinct_services,
        'current_search': search_query,
        'current_service': service_filter,
        'current_date': date_filter,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
def remove_member_view(request, room_id, user_id):
    """
    Allows the room owner to remove a member from the room.
    """
    room = get_object_or_404(Room, pk=room_id)
    user_to_remove = get_object_or_404(User, pk=user_id)

    # Security check: Only the owner can remove members, and they cannot remove themselves.
    if request.user == room.owner and user_to_remove != room.owner:
        if request.method == 'POST':
            room.members.remove(user_to_remove)
            return redirect('room_dashboard', room_id=room.id)
    else:
        # Return a 'Forbidden' error if a non-owner tries to perform this action
        return HttpResponseForbidden("You do not have permission to perform this action.")

    return redirect('room_dashboard', room_id=room.id)


@login_required
def delete_service_view(request, service_id):
    """
    Allows the room owner to delete a service and all its records.
    """
    service = get_object_or_404(Allservices, pk=service_id)
    room_id = service.room.id

    # Security check: Only the owner of the service's room can delete it.
    if request.user == service.room.owner:
        if request.method == 'POST':
            service.delete()
            return redirect('room_dashboard', room_id=room_id)
    else:
        return HttpResponseForbidden("You do not have permission to perform this action.")

    return redirect('room_dashboard', room_id=room_id)