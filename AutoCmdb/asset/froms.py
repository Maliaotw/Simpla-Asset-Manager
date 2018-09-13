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



