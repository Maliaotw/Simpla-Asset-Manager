# -*- coding:utf-8 -*-
from src.client import AutoAgent
from src.client import AutoSSH
from src.client import AutoSalt
from conf import setting


def client():
    if setting.MODE == 'agent':
        cli = AutoAgent()
    elif setting.MODE == 'ssh':
        cli = AutoSSH()
    elif setting.MODE == 'salt':
        cli = AutoSalt()
    else:
        raise Exception('请配置资产采集模式，如：ssh、agent、salt')
    cli.process()