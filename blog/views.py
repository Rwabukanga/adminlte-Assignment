from django.shortcuts import get_object_or_404, redirect, render

from django.db.models import Count, Q
from django.utils import timezone
from .forms import BlogForm, EmployeeForm, DepartmentForm
from .models import Blog, Employee, Department


# READ ALL()
def  blog_list_all(request):
    posts = Blog.objects.all().order_by('id')
    return render(request, 'blog/blog_list.html', {'posts':posts})

# READ (one)
def blog_post_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

# CREATE
def blog_post_create(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('Blog_Post_List')
    return render(request, 'blog/blog_form.html', {'form': form, 'heading': 'Create Blog Post'})


# UPDATE
def blog_post_update(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    form = BlogForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog_list_all')
    return render(request, 'blog/blog_form.html', {'form': form, 'heading': 'Edit Blog Post'})


# DELETE
def blog_post_delete(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list_all')
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})



# ---------- Department ----------

def department_list(request):
    departments = Department.objects.all().order_by('id')
    return render(request, 'blog/department_list.html', {'departments': departments})

def department_detail(request,pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'blog/department_detail.html', {department: department})

def department_create(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('Department_List')
    context = {'form': form, 'heading': 'Create Department', 'cancel_url': 'Department_List'}
    return render(request, 'blog/form.html', context)

def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('Department_List')
    context = {'form': form, 'heading': 'Edit Department', 'cancel_url': 'Department_List'}
    return render(request, 'blog/form.html', context)

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('Department_List')
    context = {
        'heading': 'Delete Department',
        'object': department,
        'employee_count': department.employees.count(),
        'cancel_url': 'Department_List',
    }
    return render(request, 'blog/blog_confirm_delete.html', context)


# ---------- Employee ----------

def employee_list(request):
    employees = Employee.objects.select_related('department').order_by('id')
    return render(request, 'blog/employee_list.html', {'employees': employees})


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'blog/employee_detail.html', {'employee': employee})


def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('Employee_List')
    context = {'form': form, 'heading': 'Create Employee', 'cancel_url': 'Employee_List'}
    return render(request, 'blog/form.html', context)


def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('Employee_List')
    context = {'form': form, 'heading': 'Edit Employee', 'cancel_url': 'Employee_List'}
    return render(request, 'blog/form.html', context)


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('Employee_List')
    context = {'heading': 'Delete Employee', 'object': employee, 'cancel_url': 'Employee_List'}
    return render(request, 'blog/confirm_delete.html', context)

# ---------- Employee ----------

def dashboard(request):
    now = timezone.now()
    per_department = Department.objects.annotate(total=Count('employees')).order_by('name')

    context = {
        'post_count': Blog.objects.count(),
        'department_count': Department.objects.count(),
        'employee_count': Employee.objects.count(),
        'posts_this_month': Blog.objects.filter(
            date_posted__year=now.year, date_posted__month=now.month
        ).count(),
        'latest_posts': Blog.objects.order_by('-date_posted')[:5],
        'latest_employees': Employee.objects.select_related('department').order_by('-hire_date')[:5],
        'chart_labels': [d.name for d in per_department],
        'chart_values': [d.total for d in per_department],
    }
    return render(request, 'blog/index.html', context)


def search(request):
    """The search box in the top bar sends ?q=... here."""
    q = request.GET.get('q', '').strip()
    posts = departments = employees = []
    if q:
        posts = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        departments = Department.objects.filter(Q(name__icontains=q) | Q(location__icontains=q))
        employees = Employee.objects.select_related('department').filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
    context = {
        'q': q,
        'posts': posts,
        'departments': departments,
        'employees': employees,
        'total': len(posts) + len(departments) + len(employees),
    }
    return render(request, 'blog/search.html', context)