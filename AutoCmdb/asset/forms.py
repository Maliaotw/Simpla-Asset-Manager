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




class DentForm(ModelForm):
    '''
    部門表單
    '''

    class Meta:
        model = models.Department
        fields = '__all__'


class CaryForm(ModelForm):
    '''
    類型表單
    '''

    class Meta:
        model = models.Catagory
        fields = '__all__'


class UserProfileForm(ModelForm):
    '''
    類型表單
    '''

    class Meta:
        model = models.UserProfile
        fields = '__all__'
