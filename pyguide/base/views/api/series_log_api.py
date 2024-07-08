from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from ...models import Material, Student_material , Exec_error_log , Series_log
import json #做 json 格式的 response 用的
import subprocess
from django.core.files.base import ContentFile
from django.core.files import File
#ipython
import select
import os
import threading
import fcntl
import time
import googletrans

# 就是一個很簡單的把資料存到資料庫的api
def save_log(request):
    if request.method == 'POST':
        student_material = Student_material.objects.get(id = request.POST.get('student_material'))
        series_log = Series_log.objects.create(
            user = request.user,
            student_material = student_material,
            cell_index = request.POST.get('cell_index'),
            log_type = request.POST.get('log_type')
        )
        return JsonResponse(request.POST)
    else:
        return JsonResponse({'res':''})