from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='First name', max_length=100, widget=forms.TextInput)
    last_name = forms.CharField(
        label='Last name', max_length=100, widget=forms.TextInput)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=32)
    SHIRT_SIZES = [
        ('XS', "Extra Small"),
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Double Extra Large"),
    ]
    shirt_size = forms.ChoiceField(choices=SHIRT_SIZES)