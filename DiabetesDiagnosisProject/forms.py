from django import forms

class DiagnosisForm(forms.Form):
    patientID = forms.IntegerField(help_text='Patient ID', required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))    

class InsertForm(forms.Form):
    """Representing the insert form"""
    pid = forms.IntegerField(help_text='Patient ID', required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))    
    age = forms.IntegerField(help_text='Age \(Minimum of 21 years\)', min_value=21, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
    bs = forms.DecimalField(help_text='Blood Sugar', decimal_places=3, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
    bp = forms.DecimalField(help_text='BS pp', decimal_places=3, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
    pr = forms.DecimalField(help_text='Plasma R', decimal_places=3, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
    pf = forms.DecimalField(help_text='Plasma F', decimal_places=3, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
    hbalc = forms.IntegerField(help_text='HbAlc', min_value=28, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))

class UpdateForm(forms.Form):
    
    FEATURE_CHOICES = [('age', 'Age'),
                        ('bs', 'Blood Sugar in Fasting'),
                        ('bp', 'Blood Sugar After Meal'),
                        ('pr', 'Plasma Glucose Test (at random)'),
                        ('pf', 'Plasma Glucose Test (before breakfast)'),
                        ('hbalc', 'Haemoglobin A1c')
                       ]

    pid = forms.IntegerField(help_text='Patient ID', required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
    #feature = forms.CharField(help_text="Feature", max_value=10, required=True, widget=forms.TextInput())
    feature = forms.CharField(widget=forms.Select(choices=FEATURE_CHOICES))
    value = forms.DecimalField(help_text='Value', decimal_places=3, required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))

class DeleteForm(forms.Form):

    pid = forms.IntegerField(help_text='Patient ID', required=True, widget=forms.NumberInput(attrs={'style': "border:0px;border-bottom:1px solid #000;text-align:center"}))
