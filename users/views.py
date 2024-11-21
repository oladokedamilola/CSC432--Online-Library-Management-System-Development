from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.views import LoginView
import pycountry
from django.contrib.auth.decorators import login_required
from books.models import UserBook

def register(request):
    print("Entering registration view")
    if request.user.is_authenticated:
        print("User is already authenticated, redirecting to home")  # Debugging statement
        return redirect('home')

    # Fetch list of countries for the registration form
    countries = [(country.alpha_2, country.name) for country in pycountry.countries]
    form = CustomUserCreationForm(request.POST or None, countries=countries)

    if request.method == 'POST':
        print("POST request received for registration")

        if form.is_valid():
            print("Registration form is valid")
            user = form.save()
            messages.success(request, "Registration successful!")
            print("Redirecting to onboarding")
            return redirect('onboarding_step1') 
        else:
            print("Registration form is invalid")
            print(form.errors)
            messages.error(request, "There were some issues with your registration. Please check the form.")
    else:
        print("GET request received for registration")
        form = CustomUserCreationForm(countries=countries)

    print("Countries loaded for form")
    return render(request, 'users/register.html', {
        'form': form,
        'countries': countries,
    })

@login_required
def onboarding_step1(request):
    if request.user.onboarding_completed:
        return redirect('home')

    if request.method == 'POST':
        form = OnboardingStep1Form(request.POST)
        if form.is_valid():
            onboarding_instance, _ = Onboarding.objects.get_or_create(user=request.user)
            onboarding_instance.is_student = form.cleaned_data['is_student']
            onboarding_instance.save()
            return redirect('onboarding_step2')
    else:
        form = OnboardingStep1Form()

    return render(request, 'users/onboarding_step1.html', {'form': form})


@login_required
def onboarding_step2(request):
    if request.user.onboarding_completed:
        return redirect('home')

    if request.method == 'POST':
        print("Form submission detected.")
        form = OnboardingStep2Form(request.POST)

        if form.is_valid():
            print("Form is valid. Processing interests.")
            # Retrieve the onboarding instance
            onboarding_instance = Onboarding.objects.get(user=request.user)
            
            # Convert the comma-separated string of interest IDs into actual UserInterest objects
            interests_ids = form.cleaned_data['interests'].split(",")  # Expecting a comma-separated string
            interests_objects = UserInterest.objects.filter(id__in=interests_ids)
            
            # Set the interests for the user
            onboarding_instance.interests.set(interests_objects)
            onboarding_instance.save()

            # Redirect to the next step in onboarding
            print("Interests saved. Redirecting to onboarding_step3.")
            return redirect('onboarding_step3')
        else:
            print("Form is not valid.")
            print(form.errors)  # This will print any form validation errors
    else:
        print("GET request detected.")
        form = OnboardingStep2Form()

    # Fetch interests to display in the template
    interests = UserInterest.objects.all()
    print(f"Fetched {len(interests)} interests.")

    return render(request, 'users/onboarding_step2.html', {'form': form, 'interests': interests})

@login_required
def onboarding_step3(request):
    if request.user.onboarding_completed:
        return redirect('home')

    if request.method == 'POST':
        form = OnboardingStep3Form(request.POST)
        if form.is_valid():
            onboarding_instance = Onboarding.objects.get(user=request.user)
            onboarding_instance.goal = form.cleaned_data['goal']
            onboarding_instance.save()

            # Mark onboarding as complete
            request.user.onboarding_completed = True
            request.user.save()
            messages.success(request, "Onboarding complete!")
            return redirect('home')
    else:
        form = OnboardingStep3Form()

    return render(request, 'users/onboarding_step3.html', {'form': form})

def custom_login_view(request):
    print("Entering custom login view")

    # Check if the user is already authenticated
    if request.user.is_authenticated:
        print("User already authenticated, checking onboarding status")
        if not request.user.onboarding_completed:
            print("Redirecting to onboarding")
            return redirect('onboarding_step1')
        print("Redirecting to home")
        return redirect('home')

    # Capture 'next' parameter
    next_url = request.GET.get('next', 'home')  # Default to 'home'

    if request.method == 'POST':
        print("POST request received")
        form = CustomLoginForm(request.POST)
        
        # Retrieve 'next' from POST data if present
        next_url = request.POST.get('next', 'home')

        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Attempting to authenticate user: {username}")

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                print(f"User authenticated: {user.username}")
                if user.is_active:
                    login(request, user)
                    print(f"Login successful for {user.username}")
                    print(f"Session ID: {request.session.session_key}")
                    
                    # Redirect to onboarding if not completed
                    if not user.onboarding_completed:
                        print("Redirecting to onboarding")
                        return redirect('onboarding_step1')

                    # Redirect to the next URL if provided, else to 'home'
                    print(f"Redirecting to: {next_url}")
                    return redirect(next_url)
                else:
                    messages.error(request, "This account is inactive.")
            else:
                print("Authentication failed")
                messages.error(request, "Invalid credentials")
        else:
            print("Form errors: ", form.errors)
    else:
        print("GET request received")
        form = CustomLoginForm()

    # Include 'next' in the context for rendering the form
    return render(request, 'users/login.html', {'form': form, 'next': next_url})

@login_required
def user_dashboard(request):
    user = request.user

    # Get books the user has liked, read, or downloaded
    liked_books = UserBook.objects.filter(user=user, liked=True)
    read_books = UserBook.objects.filter(user=user, read=True)
    downloaded_books = UserBook.objects.filter(user=user, downloaded=True)

    # Debugging: print the details of the books
    print(f"User: {user.username}")
    print(f"Liked Books: {liked_books.count()}")
    for book in liked_books:
        print(f"Liked Book: {book.book.title} by {book.book.author}")

    print(f"Read Books: {read_books.count()}")
    print(f"Downloaded Books: {downloaded_books.count()}")

    # Pass data to the template
    context = {
        'user': user,
        'liked_books': liked_books,
        'read_books': read_books,
        'downloaded_books': downloaded_books,
    }
    
    return render(request, 'users/dashboard.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)  # Added request.FILES here
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/dashboard.html', {'form': form})

# View for logging out users
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')  # Redirect back to the home page after logout










# def librarian_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('librarian_dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'users/librarian_login.html', {'form': form})


# @login_required
# def librarian_dashboard(request):
#     context = {
#             'librarian_name': request.user.username,
#             'total_books': Book.objects.count(),
#             'active_readers': Reader.objects.filter(is_active=True).count(),
#             # 'borrowed_today': BorrowedBook.objects.filter(borrow_date=date.today()).count(),
#             # 'overdue_books': BorrowedBook.objects.filter(is_overdue=True).count(),
#             # 'recent_activities': ActivityLog.objects.order_by('-timestamp')[:10], 
#             }
#     return render(request, 'users/dashboard.html', context)


# def librarian_logout(request):
#     logout(request)
#     return redirect('home')

# @login_required
# def reader_edit(request, pk):
#     reader = get_object_or_404(Reader, pk=pk)
#     if request.method == 'POST':
#         form = ReaderForm(request.POST, instance=reader)
#         if form.is_valid():
#             form.save()
#             return redirect('reader_manage')
#     else:
#         form = ReaderForm(instance=reader)
#     return render(request, 'users/reader_edit.html', {'form': form})



# @login_required(login_url='/librarian/login/')
# def reader_manage(request):
#     if request.method == 'POST':
#         form = ReaderForm(request.POST)
#         if form.is_valid():
#             reader = form.save(commit=False)
#             reader.user = request.user  # Associate the logged-in user
#             reader.save()
#             return redirect('reader_manage')
#     else:
#         form = ReaderForm()

#     readers = Reader.objects.all()
#     return render(request, 'users/reader_manage.html', {'form': form, 'readers': readers})


# @login_required(login_url='/librarian/login/')
# @require_POST
# def toggle_active(request, pk):
#     reader = get_object_or_404(Reader, pk=pk)
#     reader.is_active = not reader.is_active
#     reader.save()
#     return redirect('reader_list')