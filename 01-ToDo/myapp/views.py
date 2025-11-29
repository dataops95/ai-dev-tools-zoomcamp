from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Task


def home(request: HttpRequest) -> HttpResponse:
    """
    Home page view showing task statistics.
    """
    tasks = Task.objects.all()
    context = {
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(completed=True).count(),
        'pending_tasks': tasks.filter(completed=False).count(),
    }
    return render(request, 'home.html', context)


def task_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of all tasks.
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
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date', None)
        
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
    """
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
