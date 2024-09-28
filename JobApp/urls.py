from django.contrib import admin
from django.urls import path
from .views import  edit_internship_view,apply_view, delete_internship, delete_internship, admin_dashboard
from django.contrib.auth.views import LogoutView
from .views import login_view, register_view, admin_login_view, profile_edit_view, add_job_view, edit_job_view
from .views import delete_job, add_internship_view, apply_job, apply_internship, user_dashboard, delete_applied_job, delete_applied_internship
from .views import admin_user_detail_view, user_list_view, admin_edit_user, admin_change_password, admin_delete_user, job_detail, internship_detail
from .views import edit_user, delete_user_view, search, search_internships, search_jobs, search_listings, job_overview,internship_overview


urlpatterns = [
    #path('admin/', admin.site.urls),    
    path('login/', login_view, name='login'), 
    path('register/', register_view, name='register'),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('profile-edit/', profile_edit_view, name='admin_profile_edit'),  
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('logout/', LogoutView.as_view(next_page='/admin-login/'), name='logout'),
    path('add-job/', add_job_view, name='add_job'),
    path('edit-job/<int:pk>/', edit_job_view, name='edit_job'),
    path('add-internship/', add_internship_view, name='add_internship'),
    path('edit-internship/<int:pk>/', edit_internship_view, name='edit_internship'),
    path('apply/<str:item_type>/<int:pk>/', apply_view, name='apply'),
    path('delete-internship/<int:pk>/', delete_internship, name='delete_internship'),
    path('delete-job/<int:pk>/', delete_job, name='delete_job'),
    path('apply-job/<int:pk>/', apply_job, name='apply_job'),
    path('apply-internship/<int:pk>/', apply_internship, name='apply_internship'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
    path('delete_applied_job/<int:job_id>/', delete_applied_job, name='delete_applied_job'),
    path('delete_applied_internship/<int:internship_id>/', delete_applied_internship, name='delete_applied_internship'),
    path('admin/users/', user_list_view, name='user_list'),
    path('admin/users/<int:user_id>/', admin_user_detail_view, name='admin_user_detail'),
    path('admin/user/<int:user_id>/edit/', admin_edit_user, name='admin_edit_user'),
    path('admin/delete_user/<int:pk>/', admin_delete_user, name='admin_delete_user'),
    path('admin/user/<int:user_id>/change-password/', admin_change_password, name='admin_change_password'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    path('internship/<int:internship_id>/', internship_detail, name='internship_detail'),
    path('edit-user/<int:pk>/', edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', delete_user_view, name='delete_user'),
    path('search/jobs/', search_jobs, name='search_jobs'),
    path('search/internships/', search_internships, name='search_internships'),
    path('search/', search, name='search'),
    path('search-listings/', search_listings, name='search_listings'),
    path('jobs/<int:pk>/', job_overview, name='job_overview'),
    path('jobs/<int:pk>/', internship_overview, name='internship_overview'),
    


    path('', login_view, name='home'), 
]
