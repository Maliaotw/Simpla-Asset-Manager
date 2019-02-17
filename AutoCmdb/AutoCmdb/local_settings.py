import socket

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass

database = {
    "AWS": {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'maliaodb',
            'USER': 'root',
            'PASSWORD': '1q2w3e4r',
            'HOST': 'ec2-3-91-213-183.compute-1.amazonaws.com',
            'PORT': '3306',
        }
    },
    "TestDB": {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'testdb',
            'USER': 'root',
            'PASSWORD': '54152067',
            'HOST': '192.168.1.105',
            'PORT': '3306',
        }
    },
    "Production": {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'asset',
            'USER': 'root',
            'PASSWORD': '54152067',
            'HOST': '192.168.1.105',
            'PORT': '3306',
        }
    },
    "MAC": {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mydb',
            'USER': 'root',
            'PASSWORD': '123456',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    },

}

# AWS
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maliaodb',
        'USER': 'root',
        'PASSWORD': '1q2w3e4r',
        'HOST': 'ec2-3-91-213-183.compute-1.amazonaws.com',
        'PORT': '3306',
    }
}
'''

# 測試
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'testdb',
        'USER': 'root',
        'PASSWORD': '54152067',
        'HOST': '192.168.1.105',
        'PORT': '3306',
    }
}
'''

# 生產
'''
DATABASES =
'''

# 在家
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'mydb',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

# STATIC_ROOT = 'static'
# DEBUG = False


func = {
    'PC-073': "TestDB",
    'ip-172-31-87-103': 'AWS'
}

hostname = socket.gethostname()

DATABASES = database[func[hostname]]
# DATABASES = database[func['ip-172-31-87-103']]

#
# print(socket.gethostname())
