from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

# 課程物件
class Class_room(models.Model):
    class_room = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return self.class_room

# 用來擴增user欄位的(one to one)
class User_extension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identity_choice = (
        ("student", "student"),
        ("teacher", "teacher"),
    )
    group_choice = (
        ("experimental", "experimental"),
        ("control", "control"),
    )
    login_identity = models.CharField(max_length=20, choices=identity_choice, default="student")
    experimental_group = models.CharField(max_length=20, choices=group_choice, default="control")
    class_room = models.ManyToManyField(Class_room)

# 教師端教材物件
class Material(models.Model):
    # 和課程物件是 many to one 的關係(一堂課可以有多個教材)
    class_room = models.ForeignKey(Class_room, on_delete=models.CASCADE)
    material_name = models.CharField(max_length=50, null=True)
    material_file = models.FileField(upload_to ='work_space/teacher/materials/', null=True)
    # 運算思維類型(原本是預計一個教材對應一個運算思維，但後來發現這樣設計太白癡了，這個欄位就沒什麼用)
    CT_type = models.CharField(max_length=30, null=True)
    # 教材階段，一個整數，用來排教材顯示在前端的順序而已
    phase = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.material_name

# 學生端教材物件
class Student_material(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 教材來源，學生端教材都是從教師端的教材範本複製過來的，和教師端教材物件是 many to one 的關係(一個教師端教材物件可以給很多學生用)
    material_source = models.ForeignKey(Material, on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    student_last_modify = models.DateTimeField(auto_now=True)
    material_file = models.FileField(upload_to ='work_space/student/materials/', null=True)
    def __str__(self):
        return str(self.user) + '-' + self.material_source.material_name

# 執行核心(學生端那個連線列表裡面顯示的)
class Exec_core(models.Model):
    # 顯示在前端的名字(什麼第一組第二組之類的)
    core_name = models.CharField(max_length=50)
    # ip
    ip_address = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.core_name

# 執行錯誤紀錄(其實正確也會記錄，只是沒有錯誤訊息而已)
class Exec_error_log(models.Model):
    # 誰出錯
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 哪一個教材
    student_material = models.ForeignKey(Student_material, on_delete=models.CASCADE)
    # 錯誤訊息
    error_msg = models.CharField(max_length=200, null=True)
    # 錯誤類型
    error_type = models.CharField(max_length=50, null=True)
    # 錯誤時機
    error_time = models.CharField(max_length=20, null=True)
    # 教材中的哪一個cell
    cell_index = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user) + '-' + str(self.error_type)

# 序列資料紀錄
class Series_log(models.Model):
    # 誰的行為
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 哪一個教材
    student_material = models.ForeignKey(Student_material, on_delete=models.CASCADE)
    # 教材中的哪一個cell
    cell_index = models.IntegerField()
    # 什麼行為
    log_type = models.CharField(max_length=50, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user) + '-' + str(self.cell_index) + '-' + self.log_type

# 錯誤解釋
class Error_map_table(models.Model):
    # 錯誤類型
    error_type = models.CharField(max_length=50, null=True)
    # 短解釋(就是錯誤類型的中文翻譯)
    short_des = models.CharField(max_length=150, null=True)
    # 詳細解釋，寫在檔案中
    description = models.FileField(upload_to ='work_space/teacher/error_des/', null=True)
    def __str__(self):
        return self.error_type