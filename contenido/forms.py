from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Contenido, Categoria, VersionContenido
from ckeditor.fields import CKEditorWidget

class ContenidoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    class Meta:
        model = Contenido
        fields = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores', 'nota')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
            'solo_suscriptores': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': False, 'style': 'resize: none;'}),
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(
            is_active=True,
            moderada=True,
        )
        self.fields['nota'].label = "Nota para el siguiente usuario"
        if user.has_perm('contenido.puede_publicar_no_moderada'):
            self.fields['categoria'].queryset = Categoria.objects.filter(
                is_active=True,
            )

class ContenidoEditForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )

    class Meta:
        model = Contenido
        fields = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores', 'nota')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
            'solo_suscriptores': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': False, 'style': 'resize: none;'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(
            is_active=True,
            moderada=True,
        )
        self.fields['nota'].label = "Nota para el siguiente usuario"
        if user.has_perm('contenido.puede_publicar_no_moderada'):
            self.fields['categoria'].queryset = Categoria.objects.filter(
                is_active=True,
            )
 
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

class BorradorEditForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    class Meta:
        model = Contenido
        fields = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores', 'nota')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
            'solo_suscriptores': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': False, 'style': 'resize: none;'}),
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(
            is_active=True,
            moderada=True,
        )
        self.fields['nota'].label = "Nota para el siguiente usuario"
        if user.has_perm('contenido.puede_publicar_no_moderada'):
            self.fields['categoria'].queryset = Categoria.objects.filter(
                is_active=True,
            )

class VersionContenidoEditForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    class Meta:
        model = VersionContenido
        fields = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores', 'nota')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
            'solo_suscriptores': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': False, 'style': 'resize: none;'}),
        }
    def __init__(self, *args,  user_request=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(
            is_active=True,
            moderada=True,
        )
        self.fields['nota'].label = "Nota para el siguiente usuario"
        if user_request.has_perm('contenido.puede_publicar_no_moderada'):
            self.fields['categoria'].queryset = Categoria.objects.filter(
                is_active=True,
            )

class RechazadoEditForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(is_active=True),
        widget=forms.Select,
        empty_label="Seleccione una categoría",
        required=True,
    )
    
    class Meta:
        model = Contenido
        fields = ('titulo', 'resumen', 'categoria', 'descripcion', 'solo_suscriptores', 'nota')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'resumen': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
            'categoria': forms.Select(),
            'solo_suscriptores': forms.CheckboxInput(attrs={'class': 'form-control-2'}),
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': False, 'style': 'resize: none;'}),
        }
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(
            is_active=True,
            moderada=True,
        )
        self.fields['nota'].label = "Nota para el siguiente usuario"
        if user.has_perm('contenido.puede_publicar_no_moderada'):
            self.fields['categoria'].queryset = Categoria.objects.filter(
                is_active=True,
            )

    