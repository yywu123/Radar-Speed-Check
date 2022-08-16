from django.forms import ModelForm
from .models import CheckItem, TimeSheet
from django import forms



class ItemForm(ModelForm):

    class Meta :

        model = CheckItem
        fields = '__all__'

        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class':"form-control"}


class TimeSheetForm(ModelForm):

    class Meta:

        model = TimeSheet
        fields = '__all__'

        widgets = {
            'time': forms.TextInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': "form-control"}



