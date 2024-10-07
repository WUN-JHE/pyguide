# 功能介紹
### PyGuide – python互動式學習平台
PyGuide 使用類似 Google Colab 和 Jupyter 的介面，可以將不同類型的資源(文本、圖片、程式碼等等)組合在一個文檔當中，如此便能以各種形式解釋每一個步驟的詳細過程。同時 PyGuide 以 IPython 做為執行核心，能夠分段執行 python 程式碼，不必像傳統的 python (.py檔) 需要一次執行一整個檔案，使用者也可以更好的根據錯誤的程式碼段落做修改，降低了除錯的難度

### 系統架構
![image](https://hackmd.io/_uploads/SJyR-YFwC.png)
### 逐步學習
![image](https://hackmd.io/_uploads/H1lsmFtDA.png)
![image](https://hackmd.io/_uploads/HJ9i7FKv0.png)

### 錯誤訊息翻譯與標記
![image](https://hackmd.io/_uploads/HyQ2mttDC.png)

### 行為記錄和圖表分析
![image](https://hackmd.io/_uploads/BJGpQtFPA.png)
![image](https://hackmd.io/_uploads/SJDpQFYwC.png)
![image](https://hackmd.io/_uploads/rJRTQKFPC.png)

### 嵌入式開發板整合
![image](https://hackmd.io/_uploads/HJ3O7tKDC.png)

### 學習管理
![image](https://hackmd.io/_uploads/ry4-7KKDR.png)
![image](https://hackmd.io/_uploads/S19AzFFwC.png)
![image](https://hackmd.io/_uploads/HkagQFYw0.png)
![image](https://hackmd.io/_uploads/S1rmmtFPR.png)
![image](https://hackmd.io/_uploads/HynVQtFwA.png)

# 系統建置
## 網頁部分
### 環境設定
```
sudo apt update
sudo apt upgrade
```
裝 python 的虛擬環境 virtualenv
```
pip --version
```
or
```
pip3 --version
```
如果掃不到
```
sudo apt install python3-pip
```
```
pip -V
```
or
```
pip3 -V
```
裝virtualenv(如果你沒有)
```
pip install virtualenv
```
用 virtualenv 建立虛擬環境(如果下virtualenv指令不能用，重開)
```
virtualenv pyguide_env
```
### 資料庫
請確認你的環境是否優安裝相關的資料庫(SQLite、MySQL、MariaDB、etc...)
並且在 pyguide/pyguide/ 目錄下新增 setting.py，在裡面新增資料庫、static root等相關設定，內容請參考 Django 官方文件

### 建置pyguide
```
git clone https://github.com/WUN-JHE/pyguide.git
```
切到虛擬環境，安裝需要的 python 套件
```
cd pyguide_env
source ./bin/active
```
安裝虛擬環境所需套件
```
cd pyguide
pip install -r requirements.txt
```
生成資料庫結構
```
cd pyguide
python manage.py makemigrations
```
建立資料庫
```
python manage.py migrate
```
匯入部分固有資料
```
python manage.py loaddata base_error_map_table.json
```
新建超級使用者
```
python manage.py createsuperuser
```

先用 Django 的 runserver 啟動 web server 來做測試
```
python manage.py runserver 0.0.0.0:8000
```
打開瀏覽器 http://127.0.0.1:8000 應該要可以看到首頁
正常的話網址後面加上admin http://127.0.0.1:8000/admin
使用剛剛創建的 superuser 帳號登入後台
進到左邊Users修改你的帳號資訊
![](https://hackmd.io/_uploads/rJ5TddL3n.png)
拉到最下面
![](https://hackmd.io/_uploads/SyBA__Unn.png)
修改user_extension的欄位
login identity 選老師
experimental group 隨便選
class room 點+先隨便新增一個
改完save出來
![](https://hackmd.io/_uploads/SyR_9dU3h.png)
登出之後重新進一次原始網址
![](https://hackmd.io/_uploads/rkwes_U2h.png)
登你的超級使用者
![](https://hackmd.io/_uploads/SJ8ziOUnn.png)
完成建置

## 樹莓派部分
需要部署在任何可以執行 python 的嵌入式開發板，以樹莓派為例
下載程式碼，不需要的 pyguide 可以刪除，只需要用到 exec_core 裡面的程式
```
git clone https://github.com/WUN-JHE/pyguide.git
cd exec_core
```
安裝相關套件然後執行
```
pip install websockets ipython ansi2html
python main.py
```
執行前請先確認網路環境是否和操作網頁的設備同一個網段(ex:連到同一台AP)
並由 superuser 從後台資料表 exec_core 當中新增相對應的 core name 和 ip
之後便可以在學生端的教材編輯頁面連線樹莓派，達到在網頁中撰寫程式並且送到樹莓派執行功能
