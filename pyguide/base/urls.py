from django.urls import path
from .views.account import home as account
from .views.api import material_api, response_api, dashboard_api , series_log_api
from .views.teacher import home as teacher_home
from .views.student import home as student_home

# 這裡是處理路由的地方，不過這裡不是原始地方，這裡是後來建的，原始位置在上一層的pyguide中(和settings.py,wsgi.py同一層)

# 參數解釋
# path (路由, render頁面的那個function, for redirect 用的名字)

urlpatterns = [
    # 登入頁面
    path('', account.login_page, name = "login_page"),
    # 登出事件
    path('logout', account.logout_user, name = "logout_user"),
    # --------------------------------------------------

    # 教師端
    # 首頁
    path('teacher',teacher_home.home, name="teacher_index"),
    # 建帳號
    path('teacher/account', teacher_home.account_creation, name = "teacher_account_creation"),
    # 建課程
    path('teacher/class_room_creation', teacher_home.class_room_creation, name = "teacher_class_room_creation"),
    # 管理課程
    path('teacher/class_room/<str:class_room_pk>', teacher_home.class_room, name = "teacher_class_room"),
    # 看學生的錯誤分布(未來即時序列分析可以寫在這裡)
    path('teacher/student_dashboard/<str:student_pk>/<str:class_room_pk>', teacher_home.student_dashboard, name = "student_dashboard"),
    # 教材編輯(因應執行核心有改，未來也要做調整)
    path('teacher/material/<str:material_pk>', teacher_home.material, name = "material"),
    # --------------------------------------------------

    # 學生端
    # 首頁
    path('student',student_home.home, name="student_index"),
    # 教材列表(進入課程之後)
    path('student/class_room/<str:class_room_pk>',student_home.student_class_room, name="student_class_room"),
    # 自我檢核
    path('student/dashboard',student_home.dashboard, name="student_dashboard"),
    # 教材編輯頁面(因應執行核心修改，需大改，priority無限大)
    path('student/material/<str:material_pk>',student_home.student_material, name="student_material"),
    # --------------------------------------------------

    # 各式api，用來和後端溝通用的
    # 老師端取得教材檔案內容
    path('get_material_content/',material_api.get_material_content, name = "get_material_content"),
    # 老師端把編輯完的教材內容存回來
    path('save_material_content/',material_api.save_material_content, name = "save_material_content"),
    # 學生端取得教材檔案內容
    path('student_get_material_content/',material_api.student_get_material_content, name = "student_get_material_content"),
    # 學生端把編輯完的教材內容存回來
    path('student_save_material_content/',material_api.student_save_material_content, name = "student_save_material_content"),
    # 學生端用來把教師端教材檔案變成學生端檔案的中介點(學生第一次存取教材，會從教師的檔案目錄複製一份到學生的檔案目錄)
    path('student/access_material/<str:material_pk>',student_home.access_material, name = "access_material"),
    # 執行核心返回資訊到前端後，前端把資訊送到這裡進行翻譯和整理，然後給出反饋
    path('response_api/get_res',response_api.get_res, name = ""),
    # 教師端用來看每個學生圖表的api，返回該學生的資料
    path('dashboard_api/get_student_log_data',dashboard_api.get_student_log_data, name = ""),
    # 自我檢核頁面在用的api(for實驗組)，返回學生的錯誤圖表和重點錯誤解釋
    path('dashboard_api/get_self_log_data',dashboard_api.get_self_log_data, name = ""),
    # 自我檢核頁面在用的api(for控制組)，返回所有錯誤解釋(沒有根據學生錯誤的給，而是全部給)
    path('dashboard_api/get_self_log_des_table',dashboard_api.get_self_log_des_table, name = ""),
    # 存序列資料用的(學生端)
    path('series_log_api/save_log',series_log_api.save_log, name = ""),
    #--------------------------------------------------
]