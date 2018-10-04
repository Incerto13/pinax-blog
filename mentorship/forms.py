from django.forms import ModelForm

from .models import ConnectionRequest


class ConnectionRequestForm(ModelForm):
    class Meta:
        model = ConnectionRequest
        exclude = ('from_user', 'timestamp')