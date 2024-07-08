from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.base import ContentFile
from ...models import Class_room, User_extension, Material
from ...forms import Class_room_form, create_user_form, User_extension_Form, Material_form
from django.contrib import messages
import json


from os import path
import os

@login_required(login_url='login_page')
def home(request):
    User = get_user_model()
    students = User.objects.filter(user_extension__login_identity='student')
    class_rooms = Class_room.objects.all()
    context = {
        'login_identity' : '老師',
        'class_rooms' : class_rooms,
        'students':students,
    }
    if(request.user.user_extension.login_identity == "student"):
        return redirect('student_index')
    elif (request.user.user_extension.login_identity == "teacher"):
        return render(request, 'teacher/class_manager/home.html', context)

@login_required(login_url='login_page')
def account_creation(request):
    if request.method == 'POST':
        form = create_user_form(request.POST)
        extension_form = User_extension_Form(request.POST)
        if form.is_valid() and extension_form.is_valid():
            user = form.save()
            extension = extension_form.save(commit=False)
            extension.user = user
            extension.save()
            extension_form.save_m2m()
        else:
            print(extension_form.errors.as_data())
    else:
        form = create_user_form()
        extension_form = User_extension_Form()
    context = {
        'form':form,
        'extension_form':extension_form,
        'login_identity' : '老師',
    }
    if(request.user.user_extension.login_identity == "student"):
        return redirect('student_index')
    elif (request.user.user_extension.login_identity == "teacher"):
        return render(request, 'teacher/class_manager/account_creation.html', context)

@login_required(login_url='login_page')
def class_room_creation(request):
    if request.method == 'POST':
        print(request.POST)
        form = Class_room_form(request.POST)
        if form.is_valid():
            Class_room.objects.create(**form.cleaned_data)
            return redirect('teacher_class_room_creation')
    else:
        form = Class_room_form()
    context = {
        'login_identity' : '老師',
        'form' : form,
    }
    if(request.user.user_extension.login_identity == "student"):
        return redirect('student_index')
    elif (request.user.user_extension.login_identity == "teacher"):
        return render(request, 'teacher/class_manager/class_room_creation.html', context)

@login_required(login_url='login_page')
def class_room(request, class_room_pk):
    if request.method == 'POST':
        #print(request.FILES['material_file'].name)
        form = Material_form(request.POST,request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance2 = Class_room.objects.get(id=class_room_pk)
            instance.class_room = instance2
            if not request.FILES:
                with open('/home/mmnserver/pyguide_env/pyguide/media/work_space/sample.mmnpy', 'r') as f:
                    myfile = File(f)
                    instance.material_file.save(request.POST.get('material_name')+".mmnpy", myfile)
                
            instance.save()
            if request.FILES:
                return redirect('teacher_class_room',class_room_pk = class_room_pk)
            else:
                return redirect('teacher_class_room',class_room_pk = class_room_pk)
        else:
            print(form.errors.as_data())
    else:
        form = Material_form()
    materials = Material.objects.filter(class_room_id = class_room_pk).order_by('phase')
    my_room = Class_room.objects.get(id = class_room_pk)
    User = get_user_model()
    students = User.objects.filter(user_extension__class_room = class_room_pk)
    context = {
        'students':students,
        'materials':materials,
        'my_room':my_room,
        'form' : form,
        'login_identity' : '老師',
    }
    if(request.user.user_extension.login_identity == "student"):
        return redirect('student_index')
    elif (request.user.user_extension.login_identity == "teacher"):
        return render(request, 'teacher/class_manager/class_room.html', context)

@login_required(login_url='login_page')
def material(request, material_pk):
    material = Material.objects.get(id = material_pk)
    User = get_user_model()
    context = {
        'material':material_pk,
        'class_room':material.class_room_id,
        'login_identity' : '老師',
    }
    if(request.user.user_extension.login_identity == "student"):
        return redirect('student_index')
    elif (request.user.user_extension.login_identity == "teacher"):
        return render(request, 'teacher/class_material/home.html', context)

@login_required(login_url='login_page')
def student_dashboard(request, student_pk, class_room_pk):
    User = get_user_model()
    student = User.objects.get( id = student_pk )
    context = {
        'login_identity' : '老師',
        'student_pk':student_pk,
        'student_name':student.first_name,
        'class_room_pk':class_room_pk,
    }
    if(request.user.user_extension.login_identity == "student"):
        return redirect('student_index')
    elif (request.user.user_extension.login_identity == "teacher"):
        return render(request, 'teacher/class_manager/student_dashboard.html', context)
