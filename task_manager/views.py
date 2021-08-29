
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.gis.geos import Point

from .models import Task
from users.models import User


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        # print("LoginPage: user=>", user)
        if user is not None:
            login(request, user)
            return redirect('home')
        # else:
            # messages.info(request, 'Username or Password is incorrect')
            # pass
    context = {}
    return render(request, 'accounts/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


@login_required
def mainPage(request):

    tasks = Task.objects.all().order_by('-id')

    return render(request, 'index.html', {'tasks': tasks})


@login_required
def createTaskMap(request):
    if request.method == "POST":
        task_lat = request.POST.get("task_lat")
        task_lon = request.POST.get("task_lon")
        task_description = request.POST.get("task_description")
        task_target = request.POST.get("task_target")
        task_place = request.POST.get("task_place")
        task_plan_date = request.POST.get("task_plan_date")
        task_user = request.POST.get("task_user")
        print("createTaskMap: task_user =>", task_user)
        xuser = User.objects.filter(id=task_user).first()

        try:
            task_plan_date = datetime.strptime(task_plan_date, "%d.%m.%Y")
        except ValueError:
            return redirect('create_task_map')

        try:
            pnt = Point(float(task_lon), float(task_lat))
        except ValueError:
            return redirect('create_task_map')

        try:
            new_task = Task(
               assigned_user=xuser,
               description=task_description,
               datetime_planned=task_plan_date,
               status=2,
               point=pnt,
               mission_descr=task_target,
               place_descr=task_place,
               note="",
            )
            new_task.save()
        except Exception as e:
            print(str(e))
            return redirect('create_task_map')

        return redirect('home')
    else:
        users = User.objects.all()

    return render(request, 'create_task_map.html', {'users': users})


@login_required
def cancelTask(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        try:
            task = Task.objects.filter(id=task_id).first()
            task.status = 5
            task.save()
        except Exception as e:
            print(str(e))

    return redirect('home')
