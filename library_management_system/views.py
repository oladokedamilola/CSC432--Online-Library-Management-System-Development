from django.shortcuts import render

def home(request):
    if request.user.is_authenticated:
        print(f"User is logged in: {request.user.username}")  # Print the username to the console
    else:
        print("No user is logged in.")  # Print a message if no user is logged in
    
    return render(request, 'home.html')