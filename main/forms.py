from django import forms
from main.models import Genre, Developer, Plataform, Store



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


# formulario para establecer un rango de fechas
class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Start date",
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="End date",
        required=True
    )
    grouped = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Grouped by genres",
        required=False,
        initial=False
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Start date must be before end date.")
        return cleaned_data


# formulario para introducir un precio máximo
class MaxPriceForm(forms.Form):
    max_price = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
        label="Max price",
        required=True
    ) 


# formulario para introducir una/s palabra/s del título o descripción de un videojuego
class SearchNameOrDescriptionForm(forms.Form):
    words = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Enter a word or a sentence",
        required=True
    )


# formulario para elegir un género e introducir una/s palabra/s del título de un videojuego
class GenreAndSearchNameForm(forms.Form):
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Choose a genre",
        required=True
    )
    words = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Enter a word or words",
        required=True
    )

