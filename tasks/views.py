from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()

    return render(request, 'tasks/task_list.html', {
        'tasks':tasks
    })

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list') 
    
    else:
        form = TaskForm
        
    return render(request, 'tasks/task_create.html', {
        'form': form
    })

def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid:
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_edit.html', {
        'form': form,
        'task': task
    })


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_delete.html', {
        'task': task
    })


# Create your views here.
