from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# --- НОВОЕ: Главная страница для тех, кто не вошел ---
def welcome(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tasks/welcome.html')

# 1. READ - Список задач + СТАТИСТИКА (Шаг 37)
@login_required 
def task_list(request):
    # Получаем все задачи пользователя
    all_tasks = Task.objects.filter(user=request.user)
    
    # --- СТАТИСТИКА ---
    total_count = all_tasks.count()
    completed_count = all_tasks.filter(completed=True).count()
    uncompleted_count = total_count - completed_count
    # Считаем просроченные (не выполнены и дата меньше текущей)
    overdue_count = all_tasks.filter(completed=False, due_date__lt=timezone.now()).count()
    
    # Логика поиска
    tasks = all_tasks.order_by('-created_at')
    search_input = request.GET.get('search-area') or ''
    if search_input:
        tasks = tasks.filter(title__icontains=search_input)
    
    categories = Category.objects.all()

    return render(request, 'tasks/list.html', {
        'tasks': tasks, 
        'search_input': search_input,
        'categories': categories,
        'now': timezone.now(),
        # Передаем цифры в шаблон
        'total': total_count,
        'completed': completed_count,
        'uncompleted': uncompleted_count,
        'overdue': overdue_count,
    })

# 2. CREATE - Создание
@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Новая задача'})

# 3. UPDATE - Редактирование
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Редактировать задачу'})

# 4. DELETE - Удаление
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/delete_confirm.html', {'task': task})

# 5. TOGGLE - Статус
@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

# 6. REGISTER - Регистрация
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def welcome(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tasks/welcome.html')