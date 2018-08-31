

from conf import setting


def pack():

    response = {}

    for k,v in setting.PLUGINS.items():
        # v = 'src.plugins.disk.Diskplugin'
        # 反射
        import importlib
        m_path ,classname = v.rsplit('.',maxsplit=1)
        m = importlib.import_module(m_path)
        cls = getattr(m,classname)
        response[k] = cls().execute()

    print(response)
    return response

