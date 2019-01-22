client
===

# 說明


資產管理結合主機管理，IT人員可以對Windows主機的系統硬件資訊進行採集，並回傳給服務器，其他部門可以發起資產報修以及檢視資產維修紀錄，管理者可以管理用戶、部門、資產。

## 如何設置

**asset/roles.py**

簡易定義用戶權限。

**api/views.py**

編輯`asset_by_hostname`定義API接口。


## 如何運行

**啟動服務器**

```
python manage.py runserver 0:8000
```
