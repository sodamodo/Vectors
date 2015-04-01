from django import forms

UNITS = ((1, 'm/s'),
         (0, 'mph')

)

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
    mass = forms.CharField(max_length=256)
    velocity = forms.BooleanField(required=False)
    acceleration = forms.BooleanField(required=False)
    force = forms.BooleanField(required=False)
    coordinates = forms.BooleanField(required=False)
    units = forms.ChoiceField(choices=UNITS, widget=forms.RadioSelect())
    trajectory = forms.BooleanField(required=False)