from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Todo

# Create your views here.
def todo_list(request):
    todos = Todo.objects.filter(updated_date__lte=timezone.now()).order_by('updated_date')
    return render(request, 'todo/todo_list.html', {'todos': todos})

def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    return render(request, 'todo/todo_detail.html', {'todo': todo})
