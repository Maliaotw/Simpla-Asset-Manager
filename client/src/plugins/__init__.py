

from conf import settings


def get_server_info():

    response = {}

    for k,v in settings.PLUGINS.items():
        # v = 'src.plugins.disk.Diskplugin'
        # 反射
        # 對應配置文件
        import importlib
        m_path ,classname = v.rsplit('.',maxsplit=1)
        m = importlib.import_module(m_path)
        cls = getattr(m,classname)
        response[k] = cls().execute()

    return response

