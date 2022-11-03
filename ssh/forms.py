from django import forms
from .choices import NetmikoSupportedDevices

class SSHBaseForm(forms.Form):
	ssh_username = forms.CharField(label='SSH Username', max_length=100)
	ssh_password = forms.CharField(label='SSH Password',widget=forms.PasswordInput())
	device_type = forms.ChoiceField(
	    choices=NetmikoSupportedDevices.DEVICETYPES_CHOICES
	)
	devices  = forms.CharField(widget=forms.Textarea)
	ssh_commands  = forms.CharField(label='SSH Commands',widget=forms.Textarea)
