from django import forms

class create_video(forms.Form):
	No = forms.CharField()
	host = forms.CharField()
	ip = forms.CharField()
	start = forms.DateTimeField()
	end = forms.DateTimeField()
	px = forms.CharField()