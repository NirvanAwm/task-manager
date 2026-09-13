from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm, RegisterForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.utils import timezone
from django.contrib import messages

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    status = request.GET.get('status')

    priority = request.GET.get('priority')

    search = request.GET.get('search')

    sort = request.GET.get('sort')

    overdue = request.GET.get('overdue')

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

    elif sort == 'due_late':
        tasks = tasks.order_by(
            F('due_date').desc(nulls_last=True)
        )

    elif sort == 'due_soon':
        tasks = tasks.order_by(
            F('due_date').asc(nulls_last=True)
        )

    today = timezone.localdate()

    if overdue:
        tasks = tasks.filter(
            due_date__lt=today,
            status__in=[Task.Status.TODO, Task.Status.DOING],
        )

    overdue_count = Task.objects.filter(
        user = request.user, 
        due_date__lt=today, 
        status__in=[Task.Status.TODO, Task.Status.DOING]
    )

    paginator = Paginator(tasks, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_parms = request.GET.copy()
    query_parms.pop('page', None)

    return render(request, 'tasks/task_list.html', {
        'tasks':page_obj,
        'status': status,
        'priority': priority,
        'search': search,
        'sort': sort,
        'page_obj': page_obj,
        'query_parms': query_parms.urlencode(),
        'overdue_count': overdue_count,
        'overdue': overdue,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)

            task.user = request.user

            task.save()

            messages.success(request, 'Task created successfully.')

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

            messages.success(request, 'Task updated successfully.')

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

        messages.success(request, 'Task deleted successfully.')

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
            return redirect('dashboard')

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
            return redirect('dashboard')

    else:
        form = AuthenticationForm()

    return render(request, 'tasks/login.html', {
        'form': form
    })

def logout_view(request):

    logout(request)
    return redirect('login')

@login_required
def dashboard(request):

    task_total = Task.objects.filter(user=request.user).count()

    task_todo = Task.objects.filter(
        user=request.user,
        status=Task.Status.TODO
    ).count()

    task_doing = Task.objects.filter(
        user=request.user,
        status=Task.Status.DOING
    ).count()

    task_done = Task.objects.filter(
        user=request.user,
        status=Task.Status.DONE
    ).count()

    today = timezone.localdate()

    overdue_count = Task.objects.filter(
        user = request.user, 
        due_date__lt=today,
        status__in=[Task.Status.TODO, Task.Status.DOING]
    ).count()

    return render(request, 'tasks/dashboard.html', {
        'task_total': task_total,
        'task_todo': task_todo,
        'task_doing': task_doing,
        'task_done': task_done, 
        'overdue_count':overdue_count,
    })
# Create your views here.
