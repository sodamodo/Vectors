from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset



class DocumentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_class = 'form-inline'
        # self.helper.label_class = 'col-md-4'
        # self.helper.field_class = 'col-md-4'
        # self.helper.layout = Layout (
        #     Fieldset (
        #         'File select',
        #         'Mass',
        #         'Velocity',
        #         'Acceleration',
        #         'Coordinates',
        #         'Units',
        #         'Trajectory'
        #     )
        #
        # )

        self.helper.add_input(Submit('submit', 'Submit'))

    UNITS = ((1, 'm/s'),
            (0, 'mph')

            )

    docfile = forms.FileField(
        label='Select a file'
    )
    mass = forms.CharField(max_length=256)
    velocity = forms.BooleanField(required=False)
    acceleration = forms.BooleanField(required=False)
    force = forms.BooleanField(required=False)
    coordinates = forms.BooleanField(required=False)
    units = forms.ChoiceField(choices=((1, 'm/s'), (0, 'mph')), widget=forms.RadioSelect(), initial=1)
    trajectory = forms.BooleanField(required=False)