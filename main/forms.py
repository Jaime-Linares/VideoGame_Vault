from django import forms
from main.models import Genre



# formulario para seleccionar un género
class GenreSelectionForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose a genre",
        required=True
    )

