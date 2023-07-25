from django.shortcuts import render, get_object_or_404
from .models import Todo
from django.http import HttpResponse


def index(request):
    return render(request, 'todo/index.html', {})

def todo_list_partial(request):
    todos = Todo.objects.all()

    return render(request, 'todo/todo_list_partial.html', {'todos': todos})

def create(request):
    Todo.create(title=request.POST['title'], text=request.POST['text'])
    response = render(request, 'todo/index.html', {})
    response['HX-Redirect'] = request.META['HTTP_HX_CURRENT_URL']
    return response

def todo_details_partial(request, pk):
    todo = get_object_or_404(Todo, pk=pk)

    if request.method == 'GET':
        #RETURN FORM
        return render(request, 'todo/todo_details_partial.html', {'todo': todo})

    if request.method == 'DELETE':
        #DELETE ELEMT FROM DB
        todo.delete()

    if request.method == 'PUT':
        todo.title =  request.PUT[f'todo_{todo.pk}_title']
        todo.text = request.PUT[f'todo_{todo.pk}_text']
        todo.save()

    todos = Todo.objects.all()
    return render(request, 'todo/todo_list_partial.html', {'todos': todos})

def rerank(request):
    reranked = [int(todo) for todo in request.POST.getlist('todo_order')]
    Todo.rerank_by_list(reranked)
    return HttpResponse(status=204)


