from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.db.models import Q, Max

from django.contrib import messages

from django.utils import timezone




@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # Set the logged-in user as the sender
            message.receiver = receiver     # Set the receiver based on the username in the URL
            message.save()
            return redirect(f'/messages/?user={username}')  # Redirect to inbox after sending the message
    else:
        form = MessageForm(initial={'receiver': receiver.id})  # Set receiver in the form

    return render(request, 'profile/profile.html', {'form': form, 'receiver': receiver})



@login_required
def delete_conversation(request, user_id):
    try:
        # Assuming user_id is the ID of the user whose conversation you want to delete
        # Fetch all messages involving the logged-in user and the selected user
        messages_to_delete = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver_id=user_id)) |
            (Q(receiver=request.user) & Q(sender_id=user_id))
        )
        messages_to_delete.delete()  # Delete all messages in that conversation
        messages.success(request, "Conversation deleted successfully.")
    except Exception as e:
        messages.error(request, "Error deleting conversation.")
    return redirect('inbox')  # Adjust as necessary



#This view shows badges but they don't go away, only way is to delete the conversation
def message_index(request):
    user = request.user

    # Fetch all messages related to the logged-in user
    conversations = Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')

    # Get unique users involved in conversations
    users = {msg.sender if msg.receiver == user else msg.receiver for msg in conversations}

    selected_user = None
    messages = []

    # Filter messages based on the selected user if specified
    if request.method == 'GET' and 'user' in request.GET:
        selected_user = get_object_or_404(User, username=request.GET['user'])
        
        messages = conversations.filter(
            (Q(sender=user) & Q(receiver=selected_user)) |
            (Q(sender=selected_user) & Q(receiver=user))
        ).order_by('-timestamp')  # Order by timestamp if needed

    else:
        messages = conversations  # Show all messages if no user is selected

    # Calculate unread messages count for the logged-in user
    unread_message_count = Message.objects.filter(receiver=user, is_read=False).count()

    # Initialize the message form
    form = MessageForm()

    return render(request, 'inbox/inbox.html', {
        'conversations': messages,  # Pass filtered messages for the selected user
        'users': users,  # Pass users involved in conversations
        'selected_user': selected_user,  # The user currently selected for conversation
        'form': form,  # Pass the form to the template
        'unread_message_count': unread_message_count  # Pass unread count to the template
    })






