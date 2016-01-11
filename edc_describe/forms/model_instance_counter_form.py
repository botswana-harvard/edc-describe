from django import forms


class ModelInstanceCounterForm(forms.Form):

    producer = forms.CharField(
        max_length=50,
        label="Producer",
        initial='',
        required=False,
        help_text='This is the name of the producer / hostname , e.g. mpp50, mkl71, etc'
        )
    app_label = forms.CharField(
        max_length=50,
        label="App Label",
        initial='',
        required=False,
        help_text='All or part of the app_label. E.g maikalelo_, mpepu_, mochudi_,  etc',
        )

    key_field = forms.CharField(
        max_length=50,
        label="Key Field",
        initial='id',
        required=False,
        help_text='If your not sure just use "id"',
        )
