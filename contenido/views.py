from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import ContenidoForm, CategoriaForm, CategoriaEditForm, ContenidoEditForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Categoria, Contenido, Like
from django.urls import reverse_lazy
from django.contrib import messages

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
        else:
            form.instance.estado = 'En revisión'

            borrador_id = self.request.GET.get('borrador_id')
            rechazado_id = self.request.GET.get('rechazado_id')
            if borrador_id:
                borrador_content = get_object_or_404(Contenido, pk=borrador_id)
                borrador_content.delete()
            if rechazado_id:
                rechazado_content = get_object_or_404(Contenido, pk=rechazado_id)
                rechazado_content.delete()

        return super(ContenidoFormView,self).form_valid(form)
    
    def get_initial(self):
        borrador_content = Contenido.objects.filter(user=self.request.user, estado='Borrador').first()
        if borrador_content:
            return {
                'titulo': borrador_content.titulo,
                'categoria': borrador_content.categoria,
                'descripcion': borrador_content.descripcion,
            }
        rechazado_content = Contenido.objects.filter(user=self.request.user, estado='Rechazado').first()
        if rechazado_content:
            return {
                'titulo': rechazado_content.titulo,
                'categoria': rechazado_content.categoria,
                'descripcion': rechazado_content.descripcion,
            }
        return {}



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
    

class ListarRevisionesView(ListView):
    model = Contenido
    template_name = 'listar_revisiones.html'
    context_object_name = 'borradores'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión')
    
def publicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    # Cambiar el estado del contenido a "Publicado"
    contenido.estado = 'Publicado'
    contenido.save()

    # Redirigir a la lista de borradores
    return redirect('revisar')

def rechazar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    # Cambiar el estado del contenido a "Rechazado"
    contenido.estado = 'Rechazado'
    contenido.save()

    # Redirigir a la lista de borradores
    return redirect('revisar')

class ContenidoBorradorListView(LoginRequiredMixin, ListView):
    model = Contenido
    template_name = 'contenido/borradores_lista.html'
    context_object_name = 'contenidos_borrador'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Borrador')

class ContenidoRechazadoListView(LoginRequiredMixin, ListView):
    model = Contenido
    template_name = 'contenido/rechazados_lista.html'
    context_object_name = 'contenidos_rechazados'

    def get_queryset(self):
        # Obtener los contenidos en estado "rechazado" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Rechazado')

def detalle_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.user.is_authenticated:
        user_likes_contenido = request.user.contenido_likes.filter(id=contenido.id).exists()
    else:
        user_likes_contenido = False
    
    return render(request, 'contenido/contenido_detalle.html', {'contenido': contenido, 'user_likes_contenido': user_likes_contenido})

def toggle_like(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)

    if request.user.is_authenticated:
        try:
            # Intenta obtener el like existente del usuario para este contenido
            like = Like.objects.get(contenido=contenido, user=request.user)
            # Si el like existe, elimínalo (quitar like)
            like.delete()
            messages.success(request, 'Like eliminado correctamente.')
        except Like.DoesNotExist:
            # Si el like no existe, créalo (dar like)
            Like.objects.create(contenido=contenido, user=request.user)
            messages.success(request, 'Like agregado correctamente.')
        
        # No es necesario incrementar/decrementar el contador de likes aquí

        return redirect('detalle_contenido', pk=contenido.id)
    else:
        messages.error(request, 'Debes estar autenticado para dar/quitar like.')
        return redirect('detalle_contenido', pk=contenido.id)
    
class EditarContenidoView(UpdateView):
    model = Contenido
    form_class = ContenidoEditForm
    template_name = 'contenido/contenido_editar.html'
    success_url = reverse_lazy('index')