from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='Dashboard'),
    path('search/', views.search, name='Search'),
    path('post/', views.blog_list_all, name='Blog_Post_List'),
    path('create/', views.blog_post_create, name='Blog_Post_Create'),
    path('<int:pk>/', views.blog_post_detail, name='Blog_Post_Detail'),
    path('<int:pk>/edit/', views.blog_post_update, name='Blog_Post_Update'),
    path('<int:pk>/delete/', views.blog_post_delete, name='Blog_Post_Delete'),
    
    # ---------- Department ----------
    
    path('departments/', views.department_list, name='Department_List'),
    path('departments/create/', views.department_create, name='Department_Create'),
    path('departments/<int:pk>/', views.department_detail, name='Department_Detail'),
    path('departments/<int:pk>/edit/', views.department_update, name='Department_Update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='Department_Delete'),
    
    # ---------- Employee ----------
    
    
    path('employees/', views.employee_list, name='Employee_List'),
    path('employees/create/', views.employee_create, name='Employee_Create'),
    path('employees/<int:pk>/', views.employee_detail, name='Employee_Detail'),
    path('employees/<int:pk>/edit/', views.employee_update, name='Employee_Update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='Employee_Delete'),
]