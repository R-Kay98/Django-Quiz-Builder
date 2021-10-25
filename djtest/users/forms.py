from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from testbuilder.models import Profiles

OCCUPATION = (
   (0, 'Student'),
   (1, 'Teacher')
)

class UserRegisterForm(UserCreationForm):
	
	occupation = forms.ChoiceField(choices=OCCUPATION, widget=forms.RadioSelect())
	
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'occupation']