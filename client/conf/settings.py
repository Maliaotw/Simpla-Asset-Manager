
MODE = 'agent'


API_URL = "http://192.168.8.15:8000/api/asset_no_hostname/"
UP_API_URL = "http://192.168.8.15:8000/api/asset_by_hostname/"

KEY = "mdfmsijfiosdjoidfjdf"

AUTH_KEY_NAME = "auth-key"

PLUGINS = {
    'disk': 'src.plugins.disk.DiskPlugin',
    'mem': 'src.plugins.mem.MemPlugin',
    'nic': 'src.plugins.nic.NicPlugin',
    'basic': 'src.plugins.basic.BasicPlugin',
    'cpu': 'src.plugins.cpu.CpuPlugin',
}


