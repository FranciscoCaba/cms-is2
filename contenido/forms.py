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
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    image = forms.ImageField(label='Image',required=False)  
    video = forms.FileField(label='Video',required=False) 

    class Meta:
        model = Contenido
        fields = ('titulo', 'categoria', 'descripcion', 'image', 'video')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
        }

class ContenidoEditForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    class Meta:
        model = Contenido
        fields = ('titulo', 'categoria', 'descripcion', 'is_active', 'reportado', 'image', 'video')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
            'reportado': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
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