from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.utils.timesince import timesince

from .models import Blog, Department, Employee


def ago(moment):
    """Short 'time ago' text for the dropdowns: 'just now', '5 minutes', '3 days'."""
    if moment is None:
        return ''
    text = timesince(moment, depth=1)
    return 'just now' if text.startswith('0') else f'{text} ago'


def navbar(request):
    """Data for the top bar's Messages and Notifications dropdowns, on every page."""
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = timezone.localdate() - timedelta(days=30)

    latest_posts = list(Blog.objects.order_by('-date_posted')[:3])
    for post in latest_posts:
        post.ago = ago(post.date_posted)
    new_posts = Blog.objects.filter(date_posted__gte=week_ago).count()
    new_hires = Employee.objects.filter(hire_date__gte=month_ago).count()
    newest_hire = Employee.objects.order_by('-hire_date').values_list('hire_date', flat=True).first()

    notifications = [
        {
            'icon': 'bi-journal-text',
            'text': f'{new_posts} new post{"" if new_posts == 1 else "s"} this week',
            'url': reverse('Blog_Post_List'),
            'when': latest_posts[0].ago if latest_posts else '',
        },
        {
            'icon': 'bi-person-plus-fill',
            'text': f'{new_hires} employee{"" if new_hires == 1 else "s"} hired in 30 days',
            'url': reverse('Employee_List'),
            'when': ago(newest_hire),
        },
        {
            'icon': 'bi-building',
            'text': f'{Department.objects.count()} departments in total',
            'url': reverse('Department_List'),
            'when': '',
        },
    ]

    return {
        'nav_latest_posts': latest_posts,
        'nav_new_posts': new_posts,
        'nav_notifications': notifications,
        'nav_notification_count': new_posts + new_hires,
    }