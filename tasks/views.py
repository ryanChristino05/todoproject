from django.shortcuts import render,redirect,get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def task_list(request):
    # Récupérer les paramètres de filtrage
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    sort_by = request.GET.get('sort', 'created_at')
    
    # Filtrer les tâches de l'utilisateur
    tasks = Task.objects.filter(user=request.user)
    
    # Recherche dans titre et description
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Filtre par status
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Filtre par priority
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    
    # Tri
    if sort_by == 'title':
        tasks = tasks.order_by('title')
    elif sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'priority':
        tasks = tasks.order_by('priority')
    elif sort_by == 'status':
        tasks = tasks.order_by('status')
    else:  # created_at par défaut
        tasks = tasks.order_by('-created_at')
    
    # Calculer les statistiques
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status__in=['todo', 'in_progress']).count()
    if total_tasks > 0:
        progress = (completed_tasks / total_tasks) * 100
    else:
        progress = 0
    context = {
        'tasks': tasks,
        'search': search,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'sort_by': sort_by,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'progress': progress,
    }
    
    return render(request, 'tasks/task_list.html', context)
@login_required
def add_task(request):
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # associer l’utilisateur
            task.save()
    else:
        form=TaskForm()
    return render((request),'tasks/add_task.html',{'form':form})

@login_required
def delete_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id,user=request.user)
    task.delete()
    return redirect('tasks:task_list')

@login_required
def edit_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)  # ✅ Sécurisé
    if request.method=='POST':
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form=TaskForm(instance=task)
    return render(request,'tasks/edit_task.html',{'form':form})
    