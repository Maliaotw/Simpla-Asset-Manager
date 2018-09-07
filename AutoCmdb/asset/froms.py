from django.forms import ModelForm
from asset import models
from django import forms
from django.contrib.auth.models import User


class AssetForm(ModelForm):
    '''
    資產表單
    '''

    class Meta:
        model = models.Asset
        fields = '__all__'


class AssetHostForm(ModelForm):
    '''
    資產主機表單
    '''

    class Meta:
        model = models.AssetHost
        fields = '__all__'



