from django import forms
from .models import User_profile,Police,Address,Civilian

class User_profile_form(forms.ModelForm):
    class Meta:
        model = User_profile
        fields = ('phone_no', 'age',)


class Police_form(forms.ModelForm):
	class Meta:
		model=Police
		fields=('salary','description','post','rank')

class Civilian_form(forms.ModelForm):
	class Meta:
		model=Civilian
		fields=('job','salary')

class Address_form(forms.ModelForm):
	class Meta:
		model=Address
		fields=('house_no','locality','city','state','pin_code')