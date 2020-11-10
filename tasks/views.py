from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from .models import *
from .forms import *


# Create your views here.
def index(request):
    tasks = Task.objects.all()
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'tasks': tasks, 'form': form, 'page_obj': page_obj}
    return render(request, 'tasks/list.html', context)


def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    #by passing instance=tasl it will show the form with filled task with that id.
    form = TaskForm(instance=task)
    if request.method == 'POST':
        #need to give instance here too otherwise it will create a new task rather than updating the task
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {'form': form}
    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    context = {'task': task}
    return render(request, 'tasks/delete_task.html', context)
