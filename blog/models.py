from django.db import models
from django.utils import timezone

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    
    def __str__(self):
        return self.title
    
    
class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    hire_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees',)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'