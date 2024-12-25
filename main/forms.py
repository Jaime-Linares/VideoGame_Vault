from django import forms
from main.models import Genre, Developer



# formulario para seleccionar un género
class GenreSelectionForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose a genre",
        required=True
    )


# formulario para seleccionar un desarrollador
class DeveloperSelectionForm(forms.Form):
    developer = forms.ModelChoiceField(
        queryset=Developer.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose a developer",
        required=True
    )

    