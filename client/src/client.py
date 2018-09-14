#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : client
# @Date     : 2018/8/30
# @Author   : Maliao
# @Link     : None

import os
import json
import time
import hashlib
import requests
from src import plugins
# from lib.serialize import Json
from lib.log import Logger
from conf import settings
from concurrent.futures import ThreadPoolExecutor
import subprocess


class AutoBase(object):
    def __init__(self):
        pass

    def auth_key(self):
        current_time = time.time()
        app_id = settings.KEY
        app_id_time = "%s|%s" % (app_id, current_time)

        m = hashlib.md5()
        m.update(bytes(app_id_time, encoding='utf-8'))
        authkey = m.hexdigest()
        authkey_time = "%s|%s" % (authkey, current_time)
        return authkey_time

    def get_asset(self):
        pass

    def post_asset(self, msg, callback=None):
        """
        post方式向接口提交资产信息
        :param msg:
        :param callback:
        :return:
        """

        authkey = self.auth_key()

        r = requests.post(
            url=settings.API_URL,
            json=json.dumps(msg),
            headers={settings.AUTH_KEY_NAME: authkey}
        )
        print(r.text)

    def process(self):
        """
        派生类需要继承此方法，用于处理请求的入口
        :return:
        """
        raise NotImplementedError('you must implement process method')

    def callback(self, status, response):
        """
        提交资产后的回调函数
        :param status:
        :param response:
        :return:
        """
        pass


class AutoAgent(AutoBase):

    def process(self):
        """
        获取当前资产信息

        :return:
        """
        server_info = plugins.get_server_info()
        print(server_info)
        # self.post_asset(server_info)



class AutoSSH(AutoBase):
    pass


class AutoSalt(AutoBase):
    pass
