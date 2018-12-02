from django.forms import ModelForm
from asset import models
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# --- 資產 ---

class AssetForm(ModelForm):
    '''
    資產表單
    ['id', 'name', 'number', 'price', 'category', 'department', 'manager', 'purchase_date', 'status']
    '''

    name = forms.CharField(
        label="資產編號",
        widget=forms.TextInput(
            attrs={"readonly": 'ture', 'style': 'display:none;'}
        )
    )

    number = forms.CharField(
        label="資產號碼",
        widget=forms.NumberInput(

        )
    )

    category = forms.ModelChoiceField(
        label="類型",
        queryset=models.Category.objects.all(),
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

    number = forms.CharField(
        label="資產號碼",
        widget=forms.NumberInput(

        )
    )

    name = forms.CharField(

        widget=forms.TextInput(
            attrs={"readonly": 'ture'}
        )
    )

    def clean(self):
        cleaned_data = super().clean()

        # 驗證編號是否重複
        # 先找類型在驗證編號
        category = cleaned_data.get("category")
        number = cleaned_data.get("number")

        asset_number = models.Asset.objects.filter(category=category).filter(number=number)

        if asset_number:
            self.add_error('number', "number error")

        return cleaned_data


class Asset_Input_Form(AssetForm):

    name = forms.CharField(required=False)
    category = forms.CharField(required=False)
    department = forms.CharField(required=False)
    manager = forms.CharField(required=False)


    def clean_category(self):
        '''
        驗證類型
        :return:
        '''
        category = self.cleaned_data.get('category','')
        category_obj = models.Category.objects.filter(code=category)
        if category_obj:
            # print('category',category)
            category_obj = category_obj.first()
            self.code = category_obj.code
            return category_obj
        else:
            self.code = category
            self.add_error('category','類型代號輸入不正確')


    def clean_department(self):
        '''
        驗證部門
        :return:
        '''
        # print('department')
        status = self.data.get('status')
        if '未使用' not in status:
            department = self.cleaned_data.get('department')
            dent_obj = models.Department.objects.filter(code=department)
            if dent_obj:
                # print('department',department)
                return dent_obj.first()
            else:
                self.add_error('department', '部門代號輸入不正確')



    def valid_num(self,val,num_len=0):
        print('val', val)
        print(type(val))
        val = str(int(float(val)))
        if len(val) < num_len:
            return "%0{}d".format(num_len) % int(val)
        else:
            return val


    def clean_manager(self):
        '''
        驗證用戶
        :return:
        '''

        print('manager')
        status = self.data.get('status')
        print('status',status)
        if '未使用' not in status:
            manager = self.cleaned_data.get('manager')
            if manager:
                manager = self.valid_num(manager,num_len=3)
                user_obj = models.UserProfile.objects.filter(code=manager)
                if user_obj:
                    # print('manager',manager)
                    return user_obj.first()
                else:
                    # print('None manager')
                    self.add_error('manager', '使用者輸入不正確')
            else:
                self.add_error('manager', '使用者未輸入')


    def clean_name(self):
        '''
        name = category+ number 拼接
        :return:
        '''

        number = self.data.get('number')
        print('number',number)
        if isinstance(number,(int,float)):
            number = self.valid_num(val=number,num_len=3)
            cary = self.data.get('category')
            name = "%s-%s" % (cary, number)

            asset_obj = models.Asset.objects.filter(name=name)
            if asset_obj:
                self.add_error('number','資產編號不能重複')
                self.add_error('category','資產編號不能重複')

            return name


class Asset_Edit_Form(AssetForm):
    number = forms.CharField(
        label="資產編號",
        widget=forms.NumberInput(
            attrs={"disabled": 'ture'}
        )
    )

    category = forms.ModelChoiceField(
        label="類型",
        queryset=models.Category.objects.all(),
        widget=forms.Select(attrs={"disabled": 'ture'}),
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

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data


# --- 部門 ---

class DentForm(ModelForm):
    '''
    部門表單
    # <class 'list'>: ['id', 'name', 'code', 'block_number', 'block_number_len', 'user']
    '''

    def clean_name(self):
        '''
        驗證部門名稱
        :return:
        '''
        name = self.cleaned_data.get('name','')
        # print('name',name)

        dent_obj = models.Department.objects.filter(name=name)
        if dent_obj:
            self.add_error('name', 'name error')
        else:
            return name

    def clean_code(self):
        '''
        驗證部門簡稱
        :return:
        '''
        code = self.cleaned_data.get('code','')
        # print('name',name)

        dent_obj = models.Department.objects.filter(code=code)
        if dent_obj:
            self.add_error('code', 'code error')
        else:
            return code

    def clean(self):
        '''
        全局驗證
        :return:
        '''
        block_number = self.cleaned_data.get('block_number', '')
        block_number_len = self.cleaned_data.get("block_number_len", 0)
        print("block_number",block_number)
        print("block_number_len",block_number_len)
        if len(str(block_number)) > block_number_len:
            self.add_error('block_number','工/代號長度不得小於工/代號')
            self.add_error('block_number_len','工/代號長度不得小於工/代號')


    class Meta:
        model = models.Department
        fields = '__all__'

        error_messages = {
            'code': {
                'required': _("該欄位必填"),
            },
            'block_number': {
                'required': _("該欄位必填"),
            },
            'block_number_len': {
                'required': _("該欄位必填"),
            },
        }


class Dent_Input_Form(DentForm):
    '''
    部門匯入用表單
    '''

    user = forms.CharField(
        widget=forms.TextInput(),
        required=False
    )

    def valid_num(self,val,num_len=0):
        print('val', val)
        print(type(val))
        val = str(int(float(val)))
        if len(val) < num_len:
            return "%0{}d".format(num_len) % int(val)
        else:
            return val

    def clean_user(self):
        '''
        驗證用戶
        :return:
        '''

        print('user')

        user = self.cleaned_data.get('user')
        if user:
            user = self.valid_num(user,num_len=3)
            user_obj = models.UserProfile.objects.filter(code=user)
            if user_obj:
                # print('manager',manager)
                return user_obj.first()
            else:
                # print('None manager')
                self.add_error('user', '使用者輸入不正確')
        else:
            self.add_error('user', '使用者未輸入')




# --- 類型 ---

class CaryForm(ModelForm):
    '''
    類型表單
    '''

    def clean_code(self):
        code = self.cleaned_data['code']
        # print("code", code)

        cary_obj = models.Category.objects.filter(code=code)

        if code != 'nan' and not cary_obj:
            return code
        else:
            self.add_error('code', "code error")

    def clean_name(self):
        name = self.cleaned_data['name']
        # print(name)

        cary_obj = models.Category.objects.filter(name=name)

        if name != 'nan' and not cary_obj:
            return name
        else:
            self.add_error('name', "name error")

    class Meta:
        model = models.Category
        fields = '__all__'


# --- 用戶 ---

class UserProfileForm(ModelForm):
    '''
    UserProfile表單
    ['id', 'user', 'name', 'code', 'number', 'sex', 'dent', 'in_service', 'birthday']
    '''

    name = forms.CharField(
        label="姓名",
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        super(UserProfileForm, self).__init__(*args, **kwargs)

        # 對所有字段添加Css屬性
        for k, v in self.fields.items():
            self.fields[k].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.UserProfile
        fields = "__all__"
        exclude = ['user']


class UserProfile_Add_Form(UserProfileForm):
    dent = forms.ModelChoiceField(
        label="部門",
        queryset=models.Department.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "onchange": "get_user_number(this)"}),
        required=True,

    )

    def clean_code(self):
        '''
        驗證code是否重複
        :return:
        '''

        code = self.cleaned_data['code']
        print("code", code)
        user = models.UserProfile.objects.filter(code=code)
        if user:
            self.add_error('code', "code error")
        return code

    def clean(self):
        '''
        全局驗證
        :return:
        '''

        # 驗證number
        number = self.cleaned_data.get('number', '')
        dent = self.cleaned_data.get("dent", '')
        if not dent:
            self.add_error('dent', "dent error")
        else:
            user = models.UserProfile.objects.filter(dent=dent).filter(number=number)
            if user:
                self.add_error('number', "number error")


class UserProfile_Input_Form(ModelForm):
    '''
    用戶匯入用表單
    '''

    dent = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )

    user = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )

    number = None


    def clean_user(self):

        user = self.cleaned_data.get('user','')
        print('user',user)
        if user:
            user_obj = User.objects.filter(username=user).first()
            userpro_obj = models.UserProfile.objects.filter(user=user_obj)
            if userpro_obj:
                self.add_error('user','用戶已存在')
            elif user_obj:
                pass
            else:
                # 創建用戶
                user_obj = User.objects.create(username=user)
            return user_obj


    def clean_dent(self):
        dent = self.cleaned_data.get('dent','')
        # print('dent',dent)
        if dent:
            dent_obj = models.Department.objects.filter(code=dent)
            # print(dent_obj)
            if dent_obj:
                return dent_obj.first()
            else:
                self.add_error('dent', 'dent error')
        else:
            self.add_error('dent', 'dent error')
            raise forms.ValidationError(("部門不能為空"))

    def clean_code(self):
        code = self.cleaned_data['code']
        print('code',code)
        if code:
            user_obj = models.UserProfile.objects.filter(code=code)
            if user_obj:
                self.add_error('code','error code')
            elif len(code) > 1:
                # print('code[1:]',code[1:])
                self.number = code[1:]

        else:
            # self.number = None
            self.add_error('code', 'error code')
            self.add_error('number', 'error number')

        return code




    def clean(self):
        self.cleaned_data['number'] = self.number
        print(self.cleaned_data)

        code = self.cleaned_data['code']
        dent = self.cleaned_data['dent']
        if code and dent:
            if code[:len(dent.block_number)] != dent.block_number:
                self.add_error('code','工號與部門不一致')
                self.add_error('dent','工號與部門不一致')




    class Meta:
        model = models.UserProfile
        fields = "__all__"


class UserProfile_Edit_Form(UserProfileForm):

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
                    self.fields[k].widget.attrs.update({'disabled': 'ture'})
                    self.fields[k].widget.attrs.update({'readonly': 'ture'})


            else:
                if k in admin_readonly_fields:
                    self.fields[k].widget.attrs.update({'disabled': 'ture'})
                    self.fields[k].widget.attrs.update({'readonly': 'ture'})

            self.fields[k].widget.attrs['class'] = 'form-control'



# --- User ---


class UserForm(ModelForm):
    '''
    UsersForm
    '''

    username = forms.CharField(
        label='用戶名',
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    is_staff_choice = (
        (False, '否'),
        (True, '是'),

    )

    is_staff = forms.ChoiceField(
        label='登入',
        widget=forms.Select(
            attrs={
                "class": "col-md-10 form-control-static",
                "style": "margin-bottom: 10px",
                "onchange": "ch_login(this)",
            }
        ),
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

    class Meta:
        model = models.User
        fields = ('username', 'is_staff',)


class User_Add_Form(UserForm):

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean(self):
        is_staff = eval(self.cleaned_data.get("is_staff", False))
        if is_staff:
            passwd1 = self.cleaned_data.get('password1') if self.cleaned_data.get('password1') else '1'
            passwd2 = self.cleaned_data.get('password2') if self.cleaned_data.get('password2') else '2'
            if passwd1 != passwd2:
                # 全局錯誤
                self.add_error('password1', 'password1 error')
                self.add_error('password2', 'password2 error')
                raise forms.ValidationError(("密碼不一致"))
            else:
                self.password = self.cleaned_data.get('password1')
        else:
            self.password = "12345678"

    def save(self, commit=True):
        user_obj = super(UserForm, self).save(commit=False)
        user_obj.set_password(self.password)
        user_obj.save()
        return user_obj


class User_Edit_Form(UserForm):
    pd_status = forms.BooleanField(
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
        print('self.cleaned_data', self.cleaned_data)

        pd_status = self.cleaned_data.get("pd_status", False)
        print("pd_status", pd_status)
        if pd_status:
            passwd1 = self.cleaned_data.get('password1') if self.cleaned_data.get('password1') else '1'
            passwd2 = self.cleaned_data.get('password2') if self.cleaned_data.get('password2') else '2'
            if passwd1 != passwd2:
                # 全局錯誤
                self.add_error('password1', 'password1 error')
                self.add_error('password2', 'password2 error')
                raise forms.ValidationError(("密碼不一致"))
            else:
                self.password = self.cleaned_data.get('password1')
        else:
            self.password = ""

    def save(self, commit=True):
        user_obj = super(UserForm, self).save(commit=False)
        if self.password:
            user_obj.set_password(self.password)
        user_obj.save()


# --- 測試 ---

class Custom_User_Add_Form(forms.Form):
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
        dent = cleaned_data.get('dent', '')
        code = cleaned_data.get('code', '')

        if dent and code:
            code_num = code[len(dent.block_number):]  # 編號
            dent_num = code[:len(dent.block_number)]  # 部門號碼
            u = models.UserProfile.objects.filter(dent=dent).filter(code=code_num)

            if dent_num != dent.block_number or u:
                self.add_error('code', "code error")
            else:
                self.code = code_num
        else:
            self.add_error('code', "code error")

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
    cary = forms.ModelChoiceField(queryset=models.Category.objects.all())
