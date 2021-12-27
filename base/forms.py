from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User



class MyUserCreationForm(UserCreationForm):
    """
    Used in login_register.html for User to create account
    """
    class Meta:
        model = User
        # [password1] : Password,   [password2] : Password confirmation
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    """
    Use this class to create Form UI in room_form.html
    """

    class Meta:
        model = Room

        #Add all fields to Form UI, except those specified in [exclude]
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        # Need when User updates their profile in setting
        fields = ['avatar', 'name', 'username', 'email', 'bio']