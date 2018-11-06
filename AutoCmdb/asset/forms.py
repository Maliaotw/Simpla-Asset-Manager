from django.forms import ModelForm
from asset import models
from django import forms
from django.contrib.auth.models import User


class AssetForm(ModelForm):
    '''
    資產表單
    '''

    sn = forms.CharField(
        label="資產編號",
        widget=forms.TextInput(
            attrs={}
        )
    )

    category = forms.ModelChoiceField(
        label="類型",
        queryset=models.Catagory.objects.all(),
        widget=forms.Select(attrs={"onchange": "get_category(this)"}),
        required=True,

    )

    department = forms.ModelChoiceField(
        label="部門",
        queryset=models.Department.objects.all(),
        widget=forms.Select(attrs={"onchange": "add_assetform_user(this)", "disabled": 'ture'}),
        required=False,
    )

    manager = forms.ModelChoiceField(
        label='負責人/使用者',
        queryset=models.UserProfile.objects.all(),
        widget=forms.Select(attrs={"style": "margin-bottom: 10px", "disabled": 'ture'}),
        required=False,
    )

    status_choice = (
        ('未使用', '未使用'),
        ('使用中', '使用中'),
        ('遺失', '遺失'),
        ('報廢', '報廢'),
    )

    status = forms.ChoiceField(
        label='狀態',
        widget=forms.Select(attrs={"onchange": "ch_status_ele(this)"}),
        choices=status_choice,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(AssetForm, self).__init__(*args, **kwargs)

        admin_readonly_fields = ()
        user_readonly_fields = ()

        # print(self.request)

        # 對所有字段添加Css屬性
        for k, v in self.fields.items():

            if self.request.user.is_anonymous:
                if k in user_readonly_fields:
                    self.fields[k].widget.attrs['disabled'] = 'ture'


            else:
                if k in admin_readonly_fields:
                    self.fields[k].widget.attrs['disabled'] = 'ture'

            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Asset
        fields = '__all__'


class Asset_Add_Form(AssetForm):
    '''
    資產表單
    '''

    sn = forms.CharField(
        label="資產編號",
        widget=forms.TextInput(
            attrs={"disabled": 'ture'}
        )
    )

    def clean(self):
        cleaned_data = super().clean()

        # 驗證編號是否重複

        # 先找類型在驗證編號

        category = cleaned_data.get("category")
        sn = cleaned_data.get("sn")

        sn_num = models.Asset.objects.filter(category=category).filter(sn=sn)

        if sn_num:
            self.add_error('sn', "sn error")

        return cleaned_data


class Asset_Edit_Form(AssetForm):
    sn = forms.CharField(
        label="資產編號",
        widget=forms.TextInput(
            attrs={"readonly": 'ture'}
        )
    )

    category = forms.ModelChoiceField(
        label="類型",
        queryset=models.Catagory.objects.all(),
        widget=forms.Select(attrs={"onchange": "get_category(this)", "readonly": 'ture'}),
        required=True,

    )

    department = forms.ModelChoiceField(
        label="部門",
        queryset=models.Department.objects.all(),
        widget=forms.Select(attrs={"onchange": "add_assetform_user(this)"}),
        required=False,
    )

    manager = forms.ModelChoiceField(
        label='負責人/使用者',
        queryset=models.UserProfile.objects.all(),
        widget=forms.Select(attrs={"style": "margin-bottom: 10px"}),
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


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

    name = forms.CharField(
        label="姓名",
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(UserProfileForm, self).__init__(*args, **kwargs)

        admin_readonly_fields = ("username",)
        user_readonly_fields = ("username", "dent", "code",)

        # print(self.request)

        # 對所有字段添加Css屬性
        for k, v in self.fields.items():

            if self.request.user.is_anonymous:
                if k in user_readonly_fields:
                    self.fields[k].widget.attrs['disabled'] = 'ture'


            else:
                if k in admin_readonly_fields:
                    self.fields[k].widget.attrs['disabled'] = 'ture'

            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.UserProfile
        fields = "__all__"
        exclude = ['user']


class UserForm(ModelForm):
    '''
    UsersForm
    '''

    username = forms.CharField(
        label='用戶名',
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    is_staff_choice = (
        (True, '是'),
        (False, '否'),
    )

    is_staff = forms.ChoiceField(
        label='登入',
        widget=forms.Select(attrs={"class": "col-md-10  form-control-static", "style": "margin-bottom: 10px"}),
        choices=is_staff_choice,
        required=True,
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={"class": "col-md-10  form-control-static", "style": "margin-bottom: 10px"}),
        required=False,
    )

    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={"class": "col-md-10  form-control-static", "style": "margin-bottom: 10px"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserForm, self).__init__(*args, **kwargs)

        admin_readonly_fields = ("username",)
        user_readonly_fields = ("username",)

        # print(self.request)

        # 對所有字段添加Css屬性
        for k, v in self.fields.items():

            if self.request.user.is_anonymous:
                if k in user_readonly_fields:
                    self.fields[k].widget.attrs['disabled'] = 'ture'

            else:
                if k in admin_readonly_fields:
                    self.fields[k].widget.attrs['disabled'] = 'ture'

    def clean(self):

        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            # 全局錯誤
            raise forms.ValidationError(("密碼不一致"))

    class Meta:
        model = models.User
        fields = ('username', 'is_staff',)


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
        ('男', '男'),
        ('女', '女'),
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
        required=True,
        # disabled=True
    )

    birthday = forms.DateTimeField(
        label="生日",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    in_service_choice = (
        (None, '-----'),
        ('在職', '在職'),
        ('離職', '離職'),
        ('停職', '停職'),
        ('退休', '退休'),
    )

    in_service = forms.ChoiceField(
        label="在職狀態",
        choices=in_service_choice,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )

    is_staff_choice = (
        (None, '---'),
        (True, '是'),
        (False, '否'),
    )

    is_staff = forms.ChoiceField(
        label='登入',
        widget=forms.Select(attrs={"class": "col-md-10  form-control-static", "style": "margin-bottom: 10px",
                                   "onchange": "ch_passwd_ele(this)"}),
        choices=is_staff_choice,
        required=True,
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(
            attrs={"class": "col-md-10  form-control-static", "style": "margin-bottom: 10px"}),
        required=False,
    )

    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={"class": "col-md-10  form-control-static", "style": "margin-bottom: 10px"}),
        required=False,
    )

    def save(self, *args, **kwargs):


        if self.password1 and self.password2:
            passwd = self.password1
        else:
            passwd = "12345678"

        user = User()
        user.username = self.cleaned_data['username']
        user.set_password(passwd)
        user.is_staff = self.cleaned_data['is_staff']
        user.save()

        models.UserProfile.objects.create(
            user=user,
            name=self.cleaned_data['name'],
            sex=self.cleaned_data['sex'],
            code=self.code,
            dent=self.cleaned_data['dent'],
            birthday=self.cleaned_data['birthday'],
            in_service=self.cleaned_data['in_service']
        )


    def clean(self):
        cleaned_data = super().clean()

        # 用戶名不得重複
        user_obj = User.objects.filter(username=cleaned_data.get('username'))
        if user_obj:
            self.add_error('username', "username error")

        # 員工編號不得重複
        dent = cleaned_data.get('dent')
        code = cleaned_data.get('code')

        code_num = code[len(dent.block_number):]  # 編號
        dent_num = code[:len(dent.block_number)]  # 部門號碼
        u = models.UserProfile.objects.filter(dent=dent).filter(code=code_num)

        if dent_num != dent.block_number or u:
            self.add_error('code', "code error")
        else:
            self.code = code_num

        self.password1 = cleaned_data.get('password1', '')
        self.password2 = cleaned_data.get('password2', '')
        if self.password1 != self.password2:
            # 全局錯誤
            raise forms.ValidationError(("密碼不一致"))

    def __init__(self, *args, **kwargs):
        super(User_Add_Form, self).__init__(*args, **kwargs)

        self.fields["code"].required = True


class test1Form(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    dent = forms.ModelChoiceField(queryset=models.Department.objects.all())
    cary = forms.ModelChoiceField(queryset=models.Catagory.objects.all())
