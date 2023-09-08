from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Contenido, Categoria
from ckeditor.fields import CKEditorWidget

class ContenidoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    class Meta:
        model = Contenido
        fields = ('titulo', 'categoria', 'descripcion')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
        }

class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre','moderada']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'moderada': forms.CheckboxInput(attrs={'class': 'form-control-2'})
        }

class CategoriaEditForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre','moderada']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'moderada': forms.CheckboxInput(attrs={'class': 'form-control-2'})
        }