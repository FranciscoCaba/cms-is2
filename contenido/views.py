from django.shortcuts import render
from .forms import ContenidoForm, CategoriaForm
from django.views.generic.edit import CreateView

# Create your views here.

class ContenidoFormView(CreateView):
    template_name = 'contenido.html'
    form_class = ContenidoForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ContenidoFormView,self).form_valid(form)

class CategoriaFormView(CreateView):
    template_name = 'categoria.html'
    form_class = CategoriaForm
    success_url = '/'

    def form_valid(self, form):
        return super(CategoriaFormView,self).form_valid(form)
