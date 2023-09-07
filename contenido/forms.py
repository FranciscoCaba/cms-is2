from django import forms
from .models import Contenido
from ckeditor.fields import CKEditorWidget

class ContenidoForm(forms.ModelForm):
    
    class Meta:
        model = Contenido
        fields = ('titulo', 'descripcion')

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.CharField(widget=CKEditorWidget()),
        }