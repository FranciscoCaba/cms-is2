from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import ContenidoForm, CategoriaForm, CategoriaEditForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Categoria, Contenido
from django.urls import reverse_lazy

# Create your views here.

class ContenidoFormView(PermissionRequiredMixin, CreateView):
    permission_required = 'contenido.add_contenido'
    template_name = 'contenido/contenido_crear.html'
    form_class = ContenidoForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'

        return super(ContenidoFormView,self).form_valid(form)

class CategoriaFormView(PermissionRequiredMixin, CreateView):
    permission_required = 'contenido.add_categoria'
    template_name = 'categoria/categoria_crear.html'
    form_class = CategoriaForm
    success_url = '/contenido/categoria'

    def form_valid(self, form):
        return super(CategoriaFormView,self).form_valid(form)

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'categoria/categoria_detail.html'
    context_object_name = 'categoria'

class CategoriaUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'contenido.change_categoria'
    model = Categoria
    form_class = CategoriaEditForm
    template_name = 'categoria/categoria_edit.html'
    success_url = reverse_lazy('categoria-list')

class DesactivarCategoriaView(PermissionRequiredMixin, DetailView):
    permission_required = 'contenido.delete_categoria'
    model = Categoria
    template_name = 'categoria/desactivar_categoria.html'  # Nombre del archivo HTML que extiende de base.html

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Cambiar el estado de la categoria a inactivo
        self.object.is_active = False
        self.object.save()

        return redirect('categoria-list')

class ActivarCategoriaView(PermissionRequiredMixin, DetailView):
    permission_required = 'contenido.delete_categoria'
    model = Categoria
    template_name = 'categoria/activar_categoria.html'  # Nombre del archivo HTML que extiende de base.html

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Cambiar el estado de la categoria a activo
        self.object.is_active = True
        self.object.save()

        return redirect('categoria-list')
    
# Vista de contenidos por categoria
class MostrarContenidosView(View):
    template_name = 'mostrar_contenidos.html'

    def get(self, request, pk):
        categoria = get_object_or_404(Categoria, pk=pk)
        contenidos = Contenido.objects.filter(categoria=categoria, is_active=True, estado='Publicado')
        context = {'categoria': categoria, 'contenidos': contenidos}
        return render(request, self.template_name, context)
    

class ListarBorradoresView(ListView):
    model = Contenido
    template_name = 'listar_borradores.html'
    context_object_name = 'borradores'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión')
    
def publicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    # Cambiar el estado del contenido a "Publicado"
    contenido.estado = 'Publicado'
    contenido.save()

    # Redirigir a la lista de borradores
    return redirect('listar_borradores')

def rechazar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    # Cambiar el estado del contenido a "Rechazado"
    contenido.estado = 'Rechazado'
    contenido.save()

    # Redirigir a la lista de borradores
    return redirect('listar_borradores')