from django import forms

class EntrySearchForm(forms.Form):
    entry = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Search Encyclopedia'}))

class EntryForm(forms.Form):
    title = forms.CharField(label="")
    textarea = forms.CharField(label="", widget=forms.Textarea(attrs={'class':'textarea_new_page'}))
 
