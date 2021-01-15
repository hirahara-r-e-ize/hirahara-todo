from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Todo
from .forms import TodoForm
from django.shortcuts import redirect

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(updated_date__lte=timezone.now())
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})

def todo_add(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_date = timezone.now()
            post.save()
            return redirect('todo_detail', pk=post.pk)
    else:
        form = TodoForm()
    return render(request, 'todo/todo_add.html', {'form': form})

def todo_edit(request, pk):
    post = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_date = timezone.now()
            post.save()
            return redirect('todo_detail', pk=post.pk)
    else:
        form = TodoForm(instance=post)
    return render(request, 'todo/todo_edit.html', {'form': form})

def logout_complete(request):
    return render(request, 'todo/logout_complete.html', {})