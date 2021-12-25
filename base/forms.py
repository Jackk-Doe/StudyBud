from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

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
        fields = ['username', 'email']