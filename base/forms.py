from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    """
    Use this class to create Form UI in room_form.html
    """

    class Meta:
        model = Room

        #Add all fields to Form UI, except those specified in [exclude]
        fields = '__all__'
        exclude = ['host', 'participants']