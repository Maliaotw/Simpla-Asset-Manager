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
    UserProfile表單
    '''

    user = forms.CharField(
        label="用戶名",
        widget=forms.TextInput(
            attrs={
                # "disabled": "ture",
                "readonly": 'ture'
            }),
        # required=True,

    )

    name = forms.CharField(
        label="暱稱",
        widget=forms.TextInput(
            attrs={
                # "disabled": "ture",
                "readonly": 'ture'
            }),
    )

    admin_readonly_fields = ("")
    user_readonly_fields = ("name",)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # 對所有字段添加Css屬性
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.UserProfile
        fields = "__all__"


class UserForm(ModelForm):
    '''
    UsersForm
    '''

    is_staff_choice = (
        (True, '是'),
        (False, '否'),
    )

    is_staff = forms.ChoiceField(
        label='登入',
        widget=forms.Select(attrs={"class": "form-control"}),
        choices=is_staff_choice,
        required=True,
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),

    )

    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),

    )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.User
        fields = ('is_staff',)


class User_Add_Form(forms.Form):
    '''
    User Add 表單
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
        (None, '-----'),
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
        widget=forms.Select(attrs={"class": "form-control", "onchange": "get_user_number(this)"}),
        required=True,

    )

    code = forms.CharField(
        label="編號",
        widget=forms.TextInput(attrs={"class": "form-control", "disabled": "disabled"}),
        # disabled=True
    )

    def clean(self):
        cleaned_data = super().clean()
        user_obj = User.objects.filter(username=cleaned_data.get('username'))
        if user_obj:
            self.add_error('username', "username error")


class UserinfoForm_admin(forms.Form):
    '''

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
        (None, '-----'),
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
        widget=forms.Select(attrs={"class": "form-control", "onchange": "get_user_number(this)"}),
        required=True,

    )

    code = forms.CharField(
        label="編號",
        widget=forms.TextInput(attrs={"class": "form-control", "disabled": "disabled"}),

    )

    birthday = forms.DateTimeField(
        label="生日",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
    )

    inservice_choice = (
        (1, '在職'),
        (2, '已離職'),
    )

    inservice = forms.ChoiceField(
        label="在職狀態",
        choices=sex_choice,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,

    )

    login = forms.BooleanField(
        label="狀態",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True

    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),

    )

    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),

    ),


class test1Form(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dent = forms.ModelChoiceField(queryset=models.Department.objects.all())
    cary = forms.ModelChoiceField(queryset=models.Catagory.objects.all())
