from django import forms

class DiagnosisForm(forms.Form):
    patientID = forms.IntegerField(help_text='Patient ID within the range 1-1009', min_value=1, max_value = 1009, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))    
