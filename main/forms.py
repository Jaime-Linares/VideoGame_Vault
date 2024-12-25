from django import forms
from main.models import Genre, Developer, Plataform, Video_game, Store



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


# formulario para seleccionar una plataforma
class PlataformSelectionForm(forms.Form):
    plataform = forms.ModelChoiceField(
        queryset=Plataform.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose a plataform",
        required=True
    )


# formulario para seleccionar una tienda
class StoreSelectionForm(forms.Form):
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose a store",
        required=True
    )

   