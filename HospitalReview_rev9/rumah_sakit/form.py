from utama import models
from django import forms
from bootstrap3_datetime.widgets import DateTimeInput, DateTimePicker

class ToDoForm(forms.Form):
    todo = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    date = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    reminder = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(options={"format": "HH:mm",
                                       "pickSeconds": False}))

