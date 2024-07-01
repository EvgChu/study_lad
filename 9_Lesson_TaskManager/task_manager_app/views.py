from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm, CommentForm

def task_list(request):
    tasks = Task.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    tasks = tasks.order_by('-due_date')
    return render(request, 'task_manager_app/task/list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    comments = task.comment_set.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task 
            if request.user.is_authenticated:
                comment.creator = request.user 
            comment.save()
            return redirect('task_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'task_manager_app/task/detail.html', {'task': task, 'comments': comments, 'form': form})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.creator = request.user
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_manager_app/task/form.html', {'form': form})

def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_manager_app/task/form.html', {'form': form})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_manager_app/task/confirm_delete.html', {'task': task})

