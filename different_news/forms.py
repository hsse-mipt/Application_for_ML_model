from django import forms

ENTITY_CHOICES = (
    ("1", "Person"),
    ("2", "Organization"),
    ("3", "Profession"),
    ("4", "Country"),
    ("5", "Nationality"),
)


class QueryForm(forms.Form):
    event = forms.CharField(
        widget=forms.TextInput(attrs={"class": "header__text-input", "required": True})
    )
    entity = forms.ChoiceField(
        choices=ENTITY_CHOICES,
        widget=forms.Select(attrs={'class': 'header__form-select'})
    )
