from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label='Search Encyclopedia', max_length=100)
