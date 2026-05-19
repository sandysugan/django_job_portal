from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm
from jobs.models import Job

# ---- Job Seeker: Apply for Job ----
@login_required
def apply_job_view(request, pk):
    if not request.user.is_job_seeker():
        messages.error(request, "Only job seekers can apply.")
        return redirect('dashboard')

    job = get_object_or_404(Job, pk=pk)

    # Check duplicate application
    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('my_applications')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.status = 'Applied'
            application.save()
            messages.success(request, f'✅ Applied successfully to "{job.title}"!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply.html', {'form': form, 'job': job})


# ---- Job Seeker: My Applications ----
@login_required
def my_applications_view(request):
    if not request.user.is_job_seeker():
        return redirect('dashboard')

    applications = Application.objects.filter(
        user=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'applications/my_applications.html', {
        'applications': applications
    })


# ---- Recruiter: View Applications for a Job ----
@login_required
def job_applications_view(request, pk):
    if not request.user.is_recruiter():
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    job = get_object_or_404(Job, pk=pk)

    if job.created_by != request.user:
        return HttpResponseForbidden("You can only view applications for your own jobs.")

    applications = Application.objects.filter(job=job).select_related('user')
    return render(request, 'applications/job_applications.html', {
        'job': job,
        'applications': applications
    })


# ---- Recruiter: Update Application Status ----
@login_required
def update_status_view(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if not request.user.is_recruiter():
        return HttpResponseForbidden()

    if application.job.created_by != request.user:
        return HttpResponseForbidden("You can only update status for your job applications.")

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Status updated to {application.status}")
            return redirect('job_applications', pk=application.job.pk)
    else:
        form = ApplicationStatusForm(instance=application)

    return render(request, 'applications/update_status.html', {
        'form': form,
        'application': application
    })