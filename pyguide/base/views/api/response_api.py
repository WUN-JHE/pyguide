from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from ...models import Material, Student_material , Exec_error_log , Error_map_table
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

def get_transResult(text, dst = 'zh-TW'):
    # Initial
    translator = googletrans.Translator()
    results = translator.translate(text , dest=dst)
    return results.text

def internal_get_error_des(text):
    error_des = Error_map_table.objects.get(error_type = text)
    f = error_des.description.open('r')
    contents = f.read()
    return contents

def internal_get_error_short_des(text):
    error_des = Error_map_table.objects.get(error_type = text)
    return error_des.short_des

def msg_encode(data):
    if(data['error_msg']):
        data['error_msg'] = '<div class="d-flex flex-row mb-2"><div class="d-flex bg-white mmn-rounded p-1 me-2"><i class="bx bxs-error-alt fs-3 me-1 text-danger" ></i><span class="align-self-center">錯誤訊息</span></div><div class="d-flex"><span class="align-self-center">'+ data['error_msg'] +'</span></div></div>'
    if(data['error_type']):
        data['error_type'] = internal_get_error_short_des(data['error_type'].lower())
        data['error_type'] = '<div class="d-flex flex-row mb-2"><div class="d-flex bg-white mmn-rounded p-1 me-2"><i class="bx bxs-error-alt fs-3 me-1 text-danger" ></i><span class="align-self-center">錯誤類型</span></div><div class="d-flex"><span class="align-self-center">'+ data['error_type'] +'</span></div></div>'
    if(data['error_time']): 
        data['error_time'] = '<div class="d-flex flex-row mb-2"><div class="d-flex bg-white mmn-rounded p-1 me-2"><i class="bx bxs-error-alt fs-3 me-1 text-danger" ></i><span class="align-self-center">錯誤階段</span></div><div class="d-flex"><span class="align-self-center">'+ data['error_time'] +'</span></div></div>'
    if(data['error_lineno']):
        data['error_lineno'] = '<div class="d-flex flex-row mb-2"><div class="d-flex bg-white mmn-rounded p-1 me-2"><i class="bx bxs-error-alt fs-3 me-1 text-danger" ></i><span class="align-self-center">錯誤位置</span></div><div class="d-flex"><span class="align-self-center">第 '+ data['error_lineno'] +' 行</span></div></div>'
    data['code'] = data['error_msg'] + data['error_type'] + data['error_time'] + data['error_lineno'] + '<div class="d-flex mb-2"><div class="d-flex bg-white mmn-rounded p-1 me-2"><i class="bx bxs-comment-error fs-3 me-1 text-danger" ></i><span class="align-self-center">原始訊息</span></div></div>' + data['code']
    return data

def get_res(request):
    if request.method == 'POST':
        student_material = Student_material.objects.get(id = request.POST.get('student_material_id'))
        exec_error_log_ob = Exec_error_log.objects.create( 
            user = request.user,
            student_material = student_material,
            error_msg = request.POST.get('error_msg'),
            error_type = request.POST.get('error_type'),
            error_time = request.POST.get('error_time'),
            cell_index = request.POST.get('cell_index')
        )
        if request.user.user_extension.experimental_group == 'control':
            return_data = {
                'cell_index': request.POST.get('cell_index'),
                'code': request.POST.get('code'),
                'error_lineno': '',
                'error_msg': '',
                'error_time': '',
                'error_type': '',
                'student_material_id': request.POST.get('student_material_id'),
            }
            return JsonResponse(return_data)
        else:
            error_time_des = {
                '':'',
                'compile':'程式執行前的編譯階段',
                'runtime':'程式執行時'
            }
            return_data = {
                'cell_index': request.POST.get('cell_index'),
                'code': request.POST.get('code'),
                'error_lineno': request.POST.get('error_lineno'),
                'error_msg': get_transResult(request.POST.get('error_msg')),
                'error_time': error_time_des[request.POST.get('error_time')],
                'error_type': request.POST.get('error_type'),
                'student_material_id': request.POST.get('student_material_id'),
            }
            if(return_data['error_type']):
                return_data = msg_encode(return_data)
            
            return JsonResponse(return_data)
    else:
        return JsonResponse({'res':''})
