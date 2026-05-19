from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Job
from .forms import JobForm

# ---- Job Seekers: View All Jobs ----
@login_required
def job_list_view(request):
    if not request.user.is_job_seeker():
        messages.error(request, "Only job seekers can browse jobs.")
        return redirect('dashboard')

    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# ---- Job Details ----
@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False
    match_score = None
    matched_skills = []
    missing_skills = []

    if request.user.is_job_seeker():
        from applications.models import Application
        already_applied = Application.objects.filter(user=request.user, job=job).exists()
        result = job.calculate_match_score(request.user)
        if result:
            match_score, matched_skills, missing_skills = result

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied,
        'match_score': match_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
    })


# ---- Recruiter: Add Job ----
@login_required
def job_create_view(request):
    if not request.user.is_recruiter():
        messages.error(request, "Only recruiters can post jobs.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, f'Job "{job.title}" posted successfully!')
            return redirect('recruiter_jobs')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Add'})


# ---- Recruiter: Edit Job ----
@login_required
def job_edit_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.created_by != request.user:
        return HttpResponseForbidden("You can only edit your own jobs.")

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('recruiter_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'action': 'Edit', 'job': job})


# ---- Recruiter: Delete Job ----
@login_required
def job_delete_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if job.created_by != request.user:
        return HttpResponseForbidden("You can only delete your own jobs.")

    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f'Job "{title}" deleted.')
        return redirect('recruiter_jobs')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


# ---- Recruiter: My Jobs List ----
@login_required
def recruiter_jobs_view(request):
    if not request.user.is_recruiter():
        messages.error(request, "Access denied.")
        return redirect('dashboard')

    jobs = Job.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'jobs/recruiter_jobs.html', {'jobs': jobs})


# ---- Match Score Page ----
@login_required
def match_score_view(request, pk):
    if not request.user.is_job_seeker():
        return redirect('dashboard')

    job = get_object_or_404(Job, pk=pk)
    result = job.calculate_match_score(request.user)
    match_score, matched_skills, missing_skills = result if result else (0, [], [])

    return render(request, 'match_score.html', {
        'job': job,
        'match_score': match_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
    })