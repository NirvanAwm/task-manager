from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, RegisterForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')

    priority = request.GET.get('priority')

    search = request.GET.get('search')

    sort = request.GET.get('sort')

    if status:
        tasks = tasks.filter(status=status)

    if priority :
        tasks = tasks.filter(priority=priority)

    if search:
        tasks = tasks.filter(title__icontains=search)

    if sort == 'newest':
        tasks = tasks.order_by('-created_at')

    elif sort == 'oldest':
        tasks = tasks.order_by('created_at')

    return render(request, 'tasks/task_list.html', {
        'tasks':tasks,
        'status': status,
        'priority': priority,
        'search': search,
        'sort': sort
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)

            task.user = request.user

            task.save()
            return redirect('task_list') 
    
    else:
        form = TaskForm()
        
    return render(request, 'tasks/task_create.html', {
        'form': form
    })

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user = request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_edit.html', {
        'form': form,
        'task': task
    })


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user = request.user)

    if request.method == "POST":
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/task_delete.html', {
        'task': task
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user = request.user)

    return render(request, 'tasks/task_detail.html', {
        'task': task
    })

def register(requset):
    if requset.method == 'POST':
        form = RegisterForm(requset.POST)
        if form.is_valid():
            user = form.save()
            login(requset, user)
            return redirect('task_list')

    else:
        form = RegisterForm()

    return render(requset, 'tasks/register.html', {
        'form': form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')

    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {
        'form': form
    })

def logout_view(request):

    logout(request)
    return redirect('login')


# Create your views here.
