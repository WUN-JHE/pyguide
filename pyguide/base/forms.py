from django.forms import ModelForm
from .models import Class_room, User_extension, Material
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# 前端用的 form 格式定義

class User_extension_Form(ModelForm):
    login_identity = forms.ChoiceField(
        label = '登入身分',
        widget=forms.Select(
            attrs = {
                "class" : "form-select"
            }
        ),
        choices=[('teacher','教師'),('student','學生')]
    )
    experimental_group = forms.ChoiceField(
        label = '組別',
        widget=forms.Select(
            attrs = {
                "class" : "form-select"
            }
        ),
        choices=[('experimental','experimental'),('control','control')]
    )
    class Meta:
        model = User_extension
        fields = ['login_identity','class_room','experimental_group']
        widgets = {
            'class_room': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'class_room': '參與課程',
        }
class create_user_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(create_user_form, self).__init__( *args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = '使用者'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = '密碼'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = '確認密碼'

class Class_room_form(forms.Form):
    class_room = forms.CharField(
                    label = '課程名稱',
                    widget = forms.TextInput(
                        attrs={
                            "class" : 'form-control'
                        }
                    ),
                    help_text = "text"
                )
    description = forms.CharField(
                    label = '詳細資訊',
                    widget=forms.Textarea(
                        attrs={
                            'class' : 'form-control',
                            'rows' : 2,
                        }
                    )
                )
    location = forms.CharField(label = '上課位置',
                    widget = forms.TextInput(
                        attrs={
                            "class" : 'form-control'
                        }
                    ))

class Material_form(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['material_file', 'phase', 'CT_type', 'material_name']
        widgets = {
            'material_file':forms.FileInput(
                attrs = {
                    "class" : "form-control"
                }
            ),
            'phase':forms.NumberInput(
                attrs = {
                    "class" : "form-control"
                }
            ),
            'CT_type':forms.TextInput(
                attrs = {
                    "class" : "form-control"
                }
            ),
            'material_name':forms.TextInput(
                attrs = {
                    "class" : "form-control"
                }
            ),
        }
        labels = {
            'material_file':'匯入教材檔案',
            'material_name':'教材名稱',
            'CT_type':'運算思維',
            'phase':'課程階段',
        }
    def __init__(self, *args, **kwargs):
        super(Material_form, self).__init__( *args, **kwargs)
        self.fields['material_file'].required = False