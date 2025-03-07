from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
import json

@login_required
def task_list(request):
    tomorrow = timezone.now() + timezone.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    initial_date = tomorrow.strftime('%Y-%m-%dT%H:%M')
    
    tasks = Task.objects.filter(user=request.user)
    pending_count = tasks.filter(completed=False).count()
    completed_count = tasks.filter(completed=True).count()
    
    context = {
        'tasks': tasks,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'initial_date': initial_date,
        'form': TaskForm(initial={'due_date': initial_date}),
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'task': task, 'action': 'Update'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        return JsonResponse({'status': 'success', 'completed': task.completed})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def get_tasks_json(request):
    filter_type = request.GET.get('filter', 'all')
    
    tasks = Task.objects.filter(user=request.user)
    
    if filter_type == 'pending':
        tasks = tasks.filter(completed=False)
    elif filter_type == 'completed':
        tasks = tasks.filter(completed=True)
    
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%dT%H:%M'),
            'due_date_formatted': {
                'date': task.due_date.strftime('%a, %b %d'),
                'time': task.due_date.strftime('%I:%M %p'),
            },
            'notify_before': task.notify_before,
            'completed': task.completed,
            'is_past_due': task.is_past_due,
        })
    
    return JsonResponse({'tasks': task_list})

@login_required
def task_counts(request):
    tasks = Task.objects.filter(user=request.user)
    pending_count = tasks.filter(completed=False).count()
    completed_count = tasks.filter(completed=True).count()
    
    return JsonResponse({
        'pending_count': pending_count,
        'completed_count': completed_count,
    })
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
