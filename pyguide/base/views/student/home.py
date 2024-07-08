from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.files.base import ContentFile
from ...models import Class_room, User_extension, Material, Student_material, Exec_core

from os import path
import os


@login_required(login_url='login_page')
def home(request):
    class_rooms = request.user.user_extension.class_room.all()
    context = {
        'class_rooms' : class_rooms,
        'login_identity' : '學生',
    }
    if(request.user.user_extension.login_identity == "student"):
        return render(request, 'student/home/home.html', context)
    elif(request.user.user_extension.login_identity == "teacher"):
        return redirect('teacher_index')

@login_required(login_url='login_page')
def student_class_room(request, class_room_pk):
    # 取得所有這個課程的教材
    materials = Material.objects.filter(class_room_id = class_room_pk).order_by('phase')
    # 掃教材，排除已經被存取的
    for material in materials:
        if Student_material.objects.filter(material_source_id = material.id).filter(user_id = request.user.id):
            materials = materials.exclude(id = material.id)
    
    student_materials = Student_material.objects.filter(material_source__class_room_id = class_room_pk).filter(user_id = request.user.id).order_by('material_source__phase')

    my_room = Class_room.objects.get(id = class_room_pk)
    context = {
        'materials':materials,
        'student_materials':student_materials,
        'my_room': my_room,
        'login_identity' : '學生',
    }
    if(request.user.user_extension.login_identity == "student"):
        return render(request, 'student/home/class_room.html', context)
    elif(request.user.user_extension.login_identity == "teacher"):
        return redirect('teacher_index')

@login_required(login_url='login_page')
def access_material(request, material_pk):
    # request來源在templates/student/home/class_room.html(就是那個存取按鈕)
    # 確認student_material是否已有存取紀錄
    if ( Student_material.objects.filter( material_source_id = material_pk ).filter( user_id = request.user.id ) ):
        # 有，不動作返回
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # 沒有
        # 取出教師端教材物件(material)的檔案內容
        material = Material.objects.get(id = material_pk)
        f = material.material_file.open('r')
        contents = f.read()
        f.close()
        # 新建一個學生端教材物件(student_materail)
        student_material_ob = Student_material.objects.create( user = request.user, material_source = material)
        student_material_ob.material_file.save( str(material), ContentFile(contents), save = True )
        # 跳頁面到學生端教材編輯頁
        return redirect('student_material', material_pk = student_material_ob.id )

@login_required(login_url='login_page')
def student_material(request, material_pk):
    material = Student_material.objects.get(id = material_pk)
    exec_cores = Exec_core.objects.all().order_by('core_name')
    context = {
        'material':material_pk,
        'class_room':material.material_source.class_room_id,
        'login_identity' : '學生',
        'exec_cores' : exec_cores
    }
    if(request.user.user_extension.login_identity == "student"):
        return render(request, 'student/workspace/home.html', context)
    elif(request.user.user_extension.login_identity == "teacher"):
        return redirect('teacher_index')

@login_required(login_url='login_page')
def dashboard(request):
    
    context = {
        'login_identity' : '學生',
    }
    if(request.user.user_extension.login_identity == "student"):
        if request.user.user_extension.experimental_group == 'control':
            return render(request, 'student/home/dashboard_control.html', context)
        else:
            return render(request, 'student/home/dashboard.html', context)
    elif(request.user.user_extension.login_identity == "teacher"):
        return redirect('teacher_index')