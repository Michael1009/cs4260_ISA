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

class CreateJerseyForm(forms.Form):
    team = forms.CharField(max_length=60, widget=forms.TextInput)
    number = forms.IntegerField()
    player = forms.CharField(max_length=60, widget=forms.TextInput)
    SHIRT_SIZES = [
        ('XS', "Extra Small"),
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Double Extra Large"),
    ]
    shirt_size = forms.ChoiceField(choices=SHIRT_SIZES)
    primary_color = forms.CharField(max_length=60, widget=forms.TextInput)
    secondary_color = forms.CharField(max_length=60, widget=forms.TextInput)
    def __init__(self, *args, **kwargs):
        super(CreateJerseyForm, self).__init__(*args, **kwargs)
        self.fields['number'].widget.attrs['min'] = 0
        self.fields['number'].widget.attrs['max'] = 99
   # user_id = forms.ForeignKey(User, on_delete=models.CASCADE)