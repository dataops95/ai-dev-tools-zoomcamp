from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from typing import Any, Dict
from .models import Task

# Create your views here.
# ============================================================================
# Function-Based Views (FBV)
# ============================================================================

def task_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of all tasks.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered HTML page with task list
    """
    tasks = Task.objects.all().order_by('-created_at')
    context = {
        'tasks': tasks,
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(completed=True).count(),
    }
    return render(request, 'myapp/task_list.html', context)


def task_create(request: HttpRequest) -> HttpResponse:
    """
    Create a new task.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Redirect to task list or render form
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date', None)
        
        # Create new task
        Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date if due_date else None
        )
        return redirect('task_list')
    
    return render(request, 'myapp/task_form.html')


def task_update(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Update an existing task.
    
    Args:
        request: The HTTP request object
        pk: Primary key of the task to update
        
    Returns:
        Redirect to task list or render form
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.priority = request.POST.get('priority', 'medium')
        task.completed = request.POST.get('completed') == 'on'
        due_date = request.POST.get('due_date', None)
        task.due_date = due_date if due_date else None
        task.save()
        return redirect('task_list')
    
    context = {'task': task}
    return render(request, 'myapp/task_form.html', context)


def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Delete a task.
    
    Args:
        request: The HTTP request object
        pk: Primary key of the task to delete
        
    Returns:
        Redirect to task list
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    context = {'task': task}
    return render(request, 'myapp/task_confirm_delete.html', context)


def task_toggle_complete(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Toggle the completion status of a task.
    
    Args:
        request: The HTTP request object
        pk: Primary key of the task
        
    Returns:
        JSON response with updated status
    """
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'completed': task.completed
        })
    
    return redirect('task_list')


# ============================================================================
# Class-Based Views (CBV) - Alternative Implementation
# ============================================================================

class TaskListView(ListView):
    """Display a list of all tasks using Class-Based View."""
    model = Task
    template_name = 'myapp/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = self.get_queryset().count()
        context['completed_tasks'] = self.get_queryset().filter(completed=True).count()
        return context


class TaskCreateView(CreateView):
    """Create a new task using Class-Based View."""
    model = Task
    template_name = 'myapp/task_form.html'
    fields = ['title', 'description', 'priority', 'due_date']
    success_url = reverse_lazy('task_list')


class TaskUpdateView(UpdateView):
    """Update an existing task using Class-Based View."""
    model = Task
    template_name = 'myapp/task_form.html'
    fields = ['title', 'description', 'priority', 'completed', 'due_date']
    success_url = reverse_lazy('task_list')


class TaskDeleteView(DeleteView):
    """Delete a task using Class-Based View."""
    model = Task
    template_name = 'myapp/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
