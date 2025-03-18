from django import forms
from .models import Thoughts, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Profile_picForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Image')
    class Meta:
        model = Profile
        fields = ('profile_image', )

class ThoughtForm(forms.ModelForm):
    body = forms.CharField(required=True, widget = forms.widgets.Textarea(
            attrs={"placeholder":"Share your thoughts here!", "class":"form-control",}),
            label = "",
        )
    
    class Meta:
        model = Thoughts
        exclude = ('user',)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='', widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email address'}))
    first_name = forms.CharField(label='',max_length=100, widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Firstname'}))
    last_name = forms.CharField(label='',max_length=100, widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lastname'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

        
