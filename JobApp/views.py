from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegistrationForm, AdminLoginForm, LoginForm, ProfileForm, JobApplicationForm, InternshipApplicationForm
from .forms import JobForm, InternshipForm, UserProfileForm, UserForm, ChangePasswordForm, EditUserForm
from django.contrib.auth.decorators import login_required
from .models import Job, Internship, Application, Profile, JobApplication, InternshipApplication
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_GET
# import logging
from django.core.paginator import Paginator


@login_required
def admin_user_detail_view(request, user_id):
    # Ensure only superusers (admins) can access this view
    if not request.user.is_superuser:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get(user=user) if Profile.objects.filter(user=user).exists() else None

    # Fetch jobs and internships the user has applied for
    applied_jobs = JobApplication.objects.filter(user=user).select_related('job')
    applied_internships = InternshipApplication.objects.filter(user=user).select_related('internship')

    context = {
        'user': user,
        'profile': profile,
        'applied_jobs': applied_jobs,
        'applied_internships': applied_internships,
    }

    return render(request, 'admin_user_detail.html', context)

def job_overview(request, pk):
    # Retrieve the job by its primary key (pk)
    job = get_object_or_404(Job, pk=pk)
    # Retrieve the users who have registered for this job (if applicable)
    users = User.objects.filter(job__pk=pk)
    # Render the job overview page with job details and users
    return render(request, 'job_overview.html', {
        'job': job,
        'users': users
    })

def internship_overview(request, pk):
    # Retrieve the internship by its primary key (pk)
    internship = get_object_or_404(Internship, pk=pk)
    # Retrieve the users who have registered for this internship (if applicable)
    users = User.objects.filter(internship__pk=pk)
    # Render the internship overview page with internship details and users
    return render(request, 'internship_overview.html', {
        'internship': internship,
        'users': users
    })


def delete_user_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')  # Or whatever view you want to redirect to
    return render(request, 'confirm_delete.html', {'user': user})


@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('admin_dashboard')  # Redirect to the admin dashboard or appropriate page
    else:
        form = EditUserForm(instance=user)
    
    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
def user_dashboard(request):
    user = request.user

    # Handle form submission for profile update
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('user_dashboard')  # Redirect to avoid form resubmission
    else:
        profile_form = ProfileForm(instance=user.profile)

    # Check if the profile has a photo
    has_photo = user.profile.photo and user.profile.photo.name

    # Get search query from GET request
    search_query = request.GET.get('search', '')

    # Fetch all jobs and internships
    all_jobs = Job.objects.all().order_by('-posted_date')
    all_internships = Internship.objects.all().order_by('-posted_date')

    # Filter jobs and internships based on search query
    if search_query:
        all_jobs = all_jobs.filter(Q(title__icontains=search_query) | Q(domain_name__icontains=search_query))
        all_internships = all_internships.filter(Q(title__icontains=search_query) | Q(domain_name__icontains=search_query))

    # Get the jobs and internships the user has already applied to
    applied_jobs = JobApplication.objects.filter(user=user).values_list('job_id', flat=True)
    applied_internships = InternshipApplication.objects.filter(user=user).values_list('internship_id', flat=True)

    # Exclude the applied jobs and internships from the available lists
    available_jobs = all_jobs.exclude(id__in=applied_jobs)
    available_internships = all_internships.exclude(id__in=applied_internships)

    # Get details of the applied jobs and internships
    applied_job_details = JobApplication.objects.filter(user=user).select_related('job')
    applied_internship_details = InternshipApplication.objects.filter(user=user).select_related('internship')

    # Pagination
    job_paginator = Paginator(available_jobs, 10)  # Show 10 jobs per page
    internship_paginator = Paginator(available_internships, 10)  # Show 10 internships per page
    page_number = request.GET.get('page', 1)
    paginated_jobs = job_paginator.get_page(page_number)
    paginated_internships = internship_paginator.get_page(page_number)

    # Fetch all non-superuser users

    # Context to pass to the template
    context = {
        'profile_form': profile_form,
        'jobs': paginated_jobs,
        'internships': paginated_internships,
        'applied_jobs': applied_job_details,
        'applied_internships': applied_internship_details,
        'search_query': search_query,
        'has_photo': has_photo,
    }

    return render(request, 'user_dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and not user.is_superuser:
                auth_login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in the user
            return redirect('login')  # Redirect to user dashboard
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            # Handle invalid login
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})
    return render(request, 'admin_login.html')

@login_required
def admin_dashboard(request):
    user = request.user

    # Handle profile update
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)  # Create a new profile if not exists

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in
                return redirect('admin_dashboard')
        elif 'change_password' in request.POST:
            change_password_form = ChangePasswordForm(data=request.POST, user=request.user)
            if change_password_form.is_valid():
                change_password_form.save()
                update_session_auth_hash(request, request.user)  # Keep user logged in
                return redirect('admin_dashboard')  # Redirect to dashboard after password change
    else:
        form = ProfileForm(instance=profile)
        change_password_form = ChangePasswordForm(user=user)

    # Fetch all jobs and internships
    jobs = Job.objects.all()
    internships = Internship.objects.all()
    all_users = User.objects.exclude(is_superuser=True)

    context = {
        'form': form,
        'change_password_form': change_password_form,
        'profile': profile,
        'jobs': jobs,
        'internships': internships,
        'users': all_users,

    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Redirect to admin dashboard after saving
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_edit.html', {'form': form})

def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the same or another view
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'profile_form': form})

def admin_dashboard_view(request):
    jobs = Job.objects.all()
    internships = Internship.objects.all()
    return render(request, 'admin_dashboard.html', {
        'jobs': jobs,
        'internships': internships
    })

def add_job_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})

def edit_job_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'edit_job.html', {'form': form})

def add_internship_view(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = InternshipForm()
    return render(request, 'add_internship.html', {'form': form})

def edit_internship_view(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        form = InternshipForm(request.POST, instance=internship)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = InternshipForm(instance=internship)
    return render(request, 'edit_internship.html', {'form': form})

def apply_view(request, item_type, pk):
    if request.method == 'POST':
        additional_info = request.POST.get('additional_info')
        user = request.user
        if item_type == 'job':
            job = get_object_or_404(Job, pk=pk)
            Application.objects.create(user=user, job=job, additional_info=additional_info)
        elif item_type == 'internship':
            internship = get_object_or_404(Internship, pk=pk)
            Application.objects.create(user=user, internship=internship, additional_info=additional_info)
        return redirect('user_dashboard')  # Redirect to user dashboard or any other page
    return render(request, 'apply.html', {'item_type': item_type, 'pk': pk})

def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('admin_dashboard')  # Redirect to the admin dashboard after deletion
    return render(request, 'confirm_delete.html', {'object': job})

def delete_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        internship.delete()
        return redirect('admin_dashboard')  # Redirect to the admin dashboard after deletion
    return render(request, 'confirm_delete.html', {'object': internship})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            application.save()
            return redirect('user_dashboard')
    else:
        form = JobApplicationForm()
    
    context = {
        'form': form,
        'job': job
    }
    return render(request, 'apply_job.html', context)

@login_required
def apply_internship(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        form = InternshipApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.internship = internship
            application.save()
            return redirect('user_dashboard')
    else:
        form = InternshipApplicationForm()
    
    context = {
        'form': form,
        'internship': internship
    }
    return render(request, 'apply_internship.html', context)

def delete_applied_job(request, job_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get all job applications for the job and user
    applications = JobApplication.objects.filter(user=request.user, job_id=job_id)

    # Delete all applications found
    applications.delete()

    # Redirect back to the user dashboard
    return redirect('user_dashboard')

def delete_applied_internship(request, internship_id):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get all internship applications for the internship and user
    applications = InternshipApplication.objects.filter(user=request.user, internship_id=internship_id)

    # Delete all applications found
    applications.delete()

    # Redirect back to the user dashboard
    return redirect('user_dashboard')

@login_required
def user_list_view(request):
    # Ensure only superusers (admins) can access this view
    if not request.user.is_superuser:
        return redirect('login')
    
    # Get the search query if available
    search_query = request.GET.get('search', '')

    # Filter users by search query
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.all()

    context = {
        'users': users,
        'search_query': search_query,
    }

    return render(request, 'user_list.html', context)

@login_required
def admin_user_detail_view(request, user_id):
    # Ensure only superusers (admins) can access this view
    if not request.user.is_superuser:
        return redirect('login')

    user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get(user=user) if Profile.objects.filter(user=user).exists() else None

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'admin_user_detail.html', context)

@login_required
def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserForm(instance=user)
    
    return render(request, 'admin_edit_user.html', {'form': form, 'user': user})

@login_required
def admin_change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            return redirect('admin_dashboard')  # Redirect after password change
    else:
        form = PasswordChangeForm(user=user)
    
    return render(request, 'admin_change_password.html', {'form': form})

def admin_delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'edit_user_profile.html', {'user': user})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'job_detail.html', {'job': job})

@login_required
def internship_detail(request, internship_id):
    internship = get_object_or_404(Internship, pk=internship_id)
    return render(request, 'internship_detail.html', {'internship': internship})

def search(request):
    query = request.GET.get('query', '')
    
    # Filter jobs and internships based on the search query
    jobs = Job.objects.filter(
        title__icontains=query
    )
    
    internships = Internship.objects.filter(
        title__icontains=query
    )
    
    # If you have a domain field, include it in the filtering as well
    if query:
        jobs = jobs.filter(domain__icontains=query)
        internships = internships.filter(domain__icontains=query)
    
    # Prepare the response data
    job_data = [{
        'title': job.title,
        'location': job.location,
        'posted_on': job.posted_on.isoformat(),
        'detail_url': job.get_absolute_url(),
        'apply_url': job.get_apply_url()
    } for job in jobs]
    
    internship_data = [{
        'title': internship.title,
        'location': internship.location,
        'posted_on': internship.posted_on.isoformat(),
        'detail_url': internship.get_absolute_url(),
        'apply_url': internship.get_apply_url()
    } for internship in internships]
    
    # Return JSON response
    return JsonResponse({'jobs': job_data, 'internships': internship_data})

def search_jobs(request):
    query = request.GET.get('query', '')
    jobs = Job.objects.filter(title__icontains=query)  # Adjust the filtering as needed
    job_list = list(jobs.values('id', 'title', 'location', 'posted_date'))
    return JsonResponse({'jobs': job_list})

def search_internships(request):
    query = request.GET.get('query', '')
    internships = Internship.objects.filter(title__icontains=query)  # Adjust the filtering as needed
    internship_list = list(internships.values('id', 'title', 'location', 'posted_date'))
    return JsonResponse({'internships': internship_list})


@require_GET
def search_listings(request):
    search_query = request.GET.get('search', '')
    
    jobs = Job.objects.filter(title__icontains=search_query).values('id', 'title', 'location', 'posted_date' , 'domain_name')
    internships = Internship.objects.filter(title__icontains=search_query).values('id', 'title', 'location', 'posted_date')
    
    return JsonResponse({
        'jobs': list(jobs),
        'internships': list(internships)
    })


@login_required
def user_internships(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    internships = Internship.objects.filter(applications__user=user)  # Adjust this query based on your models
    return render(request, 'user_internships.html', {'user': user, 'internships': internships})

@login_required
def user_jobs(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    jobs = Job.objects.filter(applications__user=user)  # Adjust this query based on your models
    return render(request, 'user_jobs.html', {'user': user, 'jobs': jobs})
