from django import forms


class EmulationForm(forms.Form):
    emulate_user_name = forms.CharField(label="Emulate User", help_text="Search for user to emulate by name, username, or email and select from list.",)
    emulate_user_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
