from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import CustomUser

# ----- Register View -----
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created! Welcome, {user.username}. Please login.")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


# ----- Login View -----
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})


# ----- Logout View -----
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# ----- Dashboard View -----
@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.is_recruiter():
        from jobs.models import Job
        from applications.models import Application
        my_jobs = Job.objects.filter(created_by=user)
        total_applications = Application.objects.filter(job__created_by=user).count()
        context['my_jobs'] = my_jobs
        context['total_applications'] = total_applications
        context['total_jobs'] = my_jobs.count()
    else:
        from applications.models import Application
        my_applications = Application.objects.filter(user=user).select_related('job')
        context['my_applications'] = my_applications
        context['total_applied'] = my_applications.count()
        context['selected_count'] = my_applications.filter(status='Selected').count()
        context['rejected_count'] = my_applications.filter(status='Rejected').count()

    return render(request, 'dashboard.html', context)