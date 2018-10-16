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
    Userinfo表單
    '''

    class Meta:
        model = models.UserProfile
        fields = '__all__'


class UserForm(forms.Form):
    '''
    User表單
    '''

    username = forms.CharField(
        label="用戶名",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,

    )


    name = forms.CharField(
        label="暱稱",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,

    )

    sex_choice = (
        (1, '男'),
        (2, '女'),
    )

    sex = forms.ChoiceField(
        label="性別",
        choices=sex_choice,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,

    )


    dent = forms.ModelChoiceField(
        label="部門",
        queryset=models.Department.objects.all(),
        widget=forms.Select(attrs={"class": "form-control","onchange":"get_user_number(this)"}),
        required=True,

    )

    code = forms.CharField(
        label="編號",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        disabled=True
    )



class test1Form(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dent = forms.ModelChoiceField(queryset=models.Department.objects.all())
    cary = forms.ModelChoiceField(queryset=models.Catagory.objects.all())
