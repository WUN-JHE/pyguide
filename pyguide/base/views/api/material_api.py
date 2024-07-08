from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from ...models import Material, Student_material
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

def get_material_content(request):
    if request.method == 'POST':
        material = Material.objects.get(id = int(request.POST.get("material_id")))
        f = material.material_file.open('r')
        contents = f.read()
        return JsonResponse(json.loads(contents))
    else:
        return JsonResponse({'foo':'bar'})

def save_material_content(request):
    if request.method == 'POST':
        # 用教材ID取得教材物件
        material = Material.objects.get(id = int(request.POST.get("material_id")))
        # 打開檔案
        f = material.material_file.open(mode="r")
        # 讀檔
        contents = f.read()
        # str to dict
        contents = json.loads(contents)
        # 關閉檔案
        f.close()
        # 更新 cells 就好 ( 送到前端的只有cells，經過編輯後再送回來 )
        contents['cells'] = json.loads(request.POST.get('cells'))
        # 再次打開檔案 ( 以寫入模式開啟 )
        f = material.material_file.open(mode="w")
        # 指到檔案開頭
        f.seek(0)
        # 把更新過後內容寫回去
        f.write(json.dumps(contents))
        # 關閉檔案
        f.close()
        return HttpResponse(json.dumps("儲存成功!!"))
    else:
        return JsonResponse(json.dumps("儲存失敗!!"))


def student_get_material_content(request):
    if request.method == 'POST':
        material = Student_material.objects.get(id = int(request.POST.get("material_id")))
        f = material.material_file.open('r')
        contents = f.read()
        return JsonResponse(json.loads(contents))
    else:
        return JsonResponse({'foo':'bar'})

def student_save_material_content(request):
    if request.method == 'POST':
        # 用教材ID取得教材物件
        material = Student_material.objects.get(id = int(request.POST.get("material_id")))
        # 打開檔案
        f = material.material_file.open(mode="r")
        # 讀檔
        contents = f.read()
        # str to dict
        contents = json.loads(contents)
        # 關閉檔案
        f.close()
        # 更新 cells 就好 ( 送到前端的只有cells，經過編輯後再送回來 )
        contents['cells'] = json.loads(request.POST.get('cells'))
        # 再次打開檔案 ( 以寫入模式開啟 )
        f = material.material_file.open(mode="w")
        # 指到檔案開頭
        f.seek(0)
        # 把更新過後內容寫回去
        f.write(json.dumps(contents))
        # 關閉檔案
        f.close()
        return HttpResponse(json.dumps("儲存成功!!"))
    else:
        return JsonResponse(json.dumps("儲存失敗!!"))
