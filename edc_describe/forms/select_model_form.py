from django import forms


class SelectModelForm(forms.Form):

    app_label = forms.CharField(
        label="App label",
        required=True)

    model_name = forms.CharField(
        label="Model name",
        required=True)
