from django.shortcuts import render, redirect, get_object_or_404, redirect
from .models import Reader
from .forms import ReaderForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from books.models import Book

@login_required(login_url='/librarian/login/')
def reader_manage(request):
    if request.method == 'POST':
        form = ReaderForm(request.POST)
        if form.is_valid():
            reader = form.save(commit=False)
            reader.user = request.user  # Associate the logged-in user
            reader.save()
            return redirect('reader_manage')
    else:
        form = ReaderForm()

    readers = Reader.objects.all()
    return render(request, 'users/reader_manage.html', {'form': form, 'readers': readers})


@login_required(login_url='/librarian/login/')
@require_POST
def toggle_active(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    reader.is_active = not reader.is_active
    reader.save()
    return redirect('reader_list')


def librarian_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('librarian_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/librarian_login.html', {'form': form})


@login_required
def librarian_dashboard(request):
    context = {
            'librarian_name': request.user.username,
            'total_books': Book.objects.count(),
            'active_readers': Reader.objects.filter(is_active=True).count(),
            # 'borrowed_today': BorrowedBook.objects.filter(borrow_date=date.today()).count(),
            # 'overdue_books': BorrowedBook.objects.filter(is_overdue=True).count(),
            # 'recent_activities': ActivityLog.objects.order_by('-timestamp')[:10], 
            }
    return render(request, 'users/dashboard.html', context)


def librarian_logout(request):
    logout(request)
    return redirect('home')

@login_required
def reader_edit(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    if request.method == 'POST':
        form = ReaderForm(request.POST, instance=reader)
        if form.is_valid():
            form.save()
            return redirect('reader_manage')
    else:
        form = ReaderForm(instance=reader)
    return render(request, 'users/reader_edit.html', {'form': form})