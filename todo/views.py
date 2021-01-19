from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Todo
from .forms import TodoForm
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
from functools import reduce
from operator import and_
# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(updated_date__lte=timezone.now())
    return render(request, 'todo/todo_list.html', {'todos': todos})

def search_result(request):
    todos = Todo.objects.filter(updated_date__lte=timezone.now())
    keyword = request.GET.get('keyword')
    if keyword:
        exclusion_list = set([' ', '　'])
        q_list = ''

        for i in keyword:
            if i in exclusion_list:
                pass
            else:
                q_list += i

        query = reduce(
                    and_, [Q(title__icontains=q) | Q(text__icontains=q) | Q(author__username__icontains=q) for q in q_list]
                )
        todos = todos.filter(query)
        return render(request, 'todo/search_result.html', {'todos': todos })
    
    return render(request, 'todo/search_result.html', {'todos': todos})

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

def todo_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.complete=False
    todo.save()
    return redirect('todo_list',)

def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect('todo_list',)
