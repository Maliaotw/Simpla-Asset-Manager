client
===

# 說明

採集主機硬件資訊至資料庫。

## 如何設置

**conf/settings.py**

```
# client方式
MODE = 'agent' 

# web 接口
UP_API_URL = "http://127.0.0.1:8000/api/asset_by_hostname/"

# 請求Key
KEY = "mdfmsijfiosdjoidfjdf"
AUTH_KEY_NAME = "auth-key"

# 自定義採集模組
PLUGINS = {
    'disk': 'src.plugins.disk.DiskPlugin',
    'mem': 'src.plugins.mem.MemPlugin',
    'nic': 'src.plugins.nic.NicPlugin',
    'basic': 'src.plugins.basic.BasicPlugin',
    'cpu': 'src.plugins.cpu.CpuPlugin',
}

```

## 如何運行

**bin/update-client.py**

以當前主機名稱作為唯一，不存在即新增資料庫。

```
python bin/update-client.py
```
