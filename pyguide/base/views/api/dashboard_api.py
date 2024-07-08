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

# 去資料庫取這個error_type的中文
def internal_get_error_short_des(text):
    error_des = Error_map_table.objects.get(error_type = text)
    return error_des.short_des

# 去資料庫取這個error_type的詳細描述檔案位置，再去讀取檔案內容
def internal_get_error_des(text):
    error_des = Error_map_table.objects.get(error_type = text)
    f = error_des.description.open('r')
    contents = f.read()
    return contents

# 教師端用來取得學生錯誤類型和數量的
def get_student_log_data(request):
    if request.method == 'POST':
        # 取得學生所有錯誤紀錄(把沒有發生錯誤的結果排除)
        logs = Exec_error_log.objects.filter(user_id = request.POST.get('student_pk')).exclude(error_type = '')
        error_types = []
        return_data = []
        # 製作成echart(那個圓餅圖)可以吃的資料格式
        for log in logs:
            if log.error_type not in error_types:
                return_data.append({
                    'value' : 1,
                    'name' : log.error_type
                })
                error_types.append(log.error_type)
            else:
                for index in return_data:
                    if index['name'] == log.error_type:
                        index['value'] = index['value'] + 1
        # print(return_data)
        return JsonResponse({'data':json.dumps(return_data)})
    else:
        return JsonResponse({'data':''})

# 學生端自我檢核在用的(實驗組)
def get_self_log_data(request):
    if request.method == 'POST':
        # 取得學生所有錯誤紀錄(把沒有發生錯誤的結果排除)
        logs = Exec_error_log.objects.filter(user_id = request.user).exclude(error_type = '')
        error_types = []
        return_data = []
        return_table = []
        for log in logs:
            if log.error_type not in error_types:
                return_data.append({
                    'value' : 1,
                    'name' : log.error_type
                })
                error_types.append(log.error_type)
            else:
                for index in return_data:
                    if index['name'] == log.error_type:
                        index['value'] = index['value'] + 1
        # 錯誤類型作排序
        return_data = quick_sort(return_data)

        # 取得學生錯誤的解釋
        for data in return_data:
            return_table.append({
                'times':data['value'],
                # 錯誤類型的中文翻譯
                'type':internal_get_error_short_des(data['name']),
                # 客製化的解釋(由專家王文哲根據python built-in exception自己撰寫)
                'des':internal_get_error_des(data['name'])
            })
            data['name'] = internal_get_error_short_des(data['name'])
        return JsonResponse({'data':json.dumps(return_data),'table':json.dumps(return_table)})
    else:
        return JsonResponse({'data':''})

# 學生端自我檢核在用的(控制組)
def get_self_log_des_table(request):
    if request.method == 'POST':
        # 所有錯誤類型的解釋都抓下來
        qr_data = Error_map_table.objects.all()
        return_data = []
        # 包成前端要得格式回回去
        for data in qr_data:
            return_data.append({
                'type':internal_get_error_short_des(data.error_type),
                'des':internal_get_error_des(data.error_type)
            })
        return JsonResponse({'table':json.dumps(return_data)})
    else:
        return JsonResponse({'table':''})

# 快速排序法，前面有用到
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]['value']
        less = [x for x in arr[1:] if x['value'] >= pivot]
        greater = [x for x in arr[1:] if x['value'] < pivot]
        return quick_sort(less) + [arr[0]] + quick_sort(greater)