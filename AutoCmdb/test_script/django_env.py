#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Filename : django_env.py
# @Date     : 2018/9/13
# @Author   : Maliao
# @Link     : None

import os, threading
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.extend([BASE_DIR, ])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoCmdb.settings")

import django

django.setup()