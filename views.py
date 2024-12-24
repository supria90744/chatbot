from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Chat
from django.contrib.auth.models import User
from django.contrib import auth  

# Dummy chatbot response generator
def generate_response(message):
    # Replace this with your actual chatbot logic
    return f"Echo: {message}"

@login_required
def chatbot_view(request):
    if request.method == 'POST':
        # Process incoming message
        message = request.POST.get('message', '').strip()
        if not message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)

        # Generate chatbot response
        response = generate_response(message)

        # Save the chat to the database
        chat = Chat.objects.create(
            user=request.user,
            message=message,
            response=response
        )

        # Return the response as JSON
        return JsonResponse({'response': response})

    # For GET requests, render the chat page with chat history
    chats = Chat.objects.filter(user=request.user).order_by('id')  # Ordered by ID for chronological display
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')  # Redirect to chatbot page after successful login
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)  # Automatically log in the user after registration
                return redirect('chatbot')  # Redirect to chatbot page after registration
            except Exception as e:
                error_message = f'Error creating account: {e}'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')  # Redirect to login page after logout
