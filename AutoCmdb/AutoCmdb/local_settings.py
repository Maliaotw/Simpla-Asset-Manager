
try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    pass


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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'asset',
        'USER': 'root',
        'PASSWORD': '54152067',
        'HOST': '192.168.1.105',
        'PORT': '3306',
    }
}
'''

# 在家
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# STATIC_ROOT = 'static'
# DEBUG = False
