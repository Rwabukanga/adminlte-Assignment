from django import forms

from .models import Blog, Employee, Department




class BootstrapFormMixin:
    """Adds AdminLTE/Bootstrap CSS classes to every field of the form."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

class BlogForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']

class DepartmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'location']
        
class EmployeeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'hire_date', 'department']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }