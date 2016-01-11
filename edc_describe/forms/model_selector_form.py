from django import forms


class ModelSelectorForm(forms.Form):

    app_label = forms.CharField(
        max_length=50,
        label="App",
        required=True)

    model_name = forms.CharField(
        max_length=50,
        label="Model",
        required=True)
