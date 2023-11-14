from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from .forms import ContenidoForm, CategoriaForm, CategoriaEditForm, ContenidoEditForm, BorradorEditForm, RechazadoEditForm, VersionContenidoEditForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, View
from .models import Categoria, Contenido, Like,Dislike ,VersionContenido, Image, Video, Archivos, Favoritos, Calificacion
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden, HttpResponse,JsonResponse
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO
import qrcode
from django.core.files import File

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
        if 'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                form.instance.estado = 'En revisión'
            else:
                form.instance.estado = 'Publicado'
        contenido = form.save(commit=False)
        contenido.save_version(user=self.request.user)
        if  'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
                context = {
                    'titulo': form.instance.titulo,
                    'content_url': content_url,
                }      
                html_template = 'notificaciones/en_revision.html'
                html_message = render_to_string(html_template, context)
                subject = 'Cambio de estado de publicación'
                message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [self.request.user.email])
                message.content_subtype = 'html'
                message.send()
            else:
                content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
                context = {
                    'titulo': form.instance.titulo,
                    'content_url': content_url,
                }      
                html_template = 'notificaciones/publicado_no_moderada.html'
                html_message = render_to_string(html_template, context)
                subject = 'Cambio de estado de publicación'
                message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [self.request.user.email])
                message.content_subtype = 'html'
                message.send()
        if 'borradorcito' in self.request.POST:
            content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
            context = {
                    'titulo': contenido.titulo,
                    'content_url': content_url,
                }      
            html_template = 'notificaciones/borrador.html'
            html_message = render_to_string(html_template, context)
            subject = 'Cambio de estado de publicación'
            message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
            message.content_subtype = 'html'
            message.send()
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=contenido, image=image)
        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=contenido, video=video)
        for archivo in self.request.FILES.getlist('archivos'):
            Archivos.objects.create(contenido=contenido, archivo=archivo)
        return redirect('/')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        if self.object.estado == 'Borrador':
            return reverse_lazy('borradores_lista')  # Reemplaza 'borrador-lista' con tu nombre de URL correcto
        else:
            return reverse_lazy('index')  # Reemplaza 'index' con tu nombre de URL correcto

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
        if request.user.is_authenticated:
            user_favorito_categoria = request.user.categoria_favoritos.filter(id=categoria.id).exists()
        else:
            user_favorito_categoria = False
        contenidos = Contenido.objects.filter(categoria=categoria, is_active=True, estado='Publicado').order_by('-fecha')
        context = {'categoria': categoria, 'contenidos': contenidos, 'user_favorito_categoria': user_favorito_categoria}
        return render(request, self.template_name, context)
    

class ListarRevisionesView(PermissionRequiredMixin,ListView):
    model = Contenido
    permission_required = 'contenido.ver_revisiones'
    template_name = 'listar_revisiones.html'
    context_object_name = 'por_revisar'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión').order_by('-fecha')
    
class ListarUnaRevisionView(PermissionRequiredMixin,ListView):
    model = Contenido
    permission_required = 'contenido.ver_revisiones'
    template_name = 'listar_revisiones.html'
    context_object_name = 'por_revisar'

    def get_queryset(self):
        return Contenido.objects.filter(estado='En revisión', id=self.kwargs['pk']).order_by('-fecha')

class ContenidosApublicarView(ListView):
    model = Contenido
    template_name = 'contenido/contenido_a_publicar.html'
    context_object_name = 'revisados'

    def get_queryset(self):
        return Contenido.objects.filter(estado='A publicar').order_by('-fecha')
    
class UnContenidoApublicarView(ListView):
    model = Contenido
    template_name = 'contenido/contenido_a_publicar.html'
    context_object_name = 'revisados'

    def get_queryset(self):
        return Contenido.objects.filter(estado='A publicar', id=self.kwargs['pk']).order_by('-fecha')

@permission_required('contenido.puede_editar_aceptar')
def apublicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    if request.method == 'POST':
        nota = request.POST.get('nota')
        contenido.nota = nota
        # Cambiar el estado del contenido a "A publicar"
        contenido.estado = 'A publicar'
        contenido.save(user=request.user)
        content_url = request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
        context = {
            'titulo': contenido.titulo,
            'content_url': content_url,    
        }      
        html_template = 'notificaciones/a_publicar.html'
        html_message = render_to_string(html_template, context)
        subject = 'Cambio de estado de publicación'
        message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
        message.content_subtype = 'html'
        message.send()

        # Redirigir a la lista de revisiones
        return redirect('listar_revisiones')
    
    return render(request, 'contenido/dar_nota_form.html', {'contenido': contenido, 'opcion': 'revision'})

@permission_required('contenido.puede_publicar_rechazar')
def publicar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    if request.method == 'POST':
        nota = request.POST.get('nota')
        contenido.nota = nota
        # Cambiar el estado del contenido a "Publicado"
        contenido.estado = 'Publicado'
        contenido.save_version(user=request.user)
        content_url = request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
        context = {
            'titulo': contenido.titulo,
            'nota': contenido.nota,
            'content_url': content_url,   
        }      
        html_template = 'notificaciones/publicado.html'
        html_message = render_to_string(html_template, context)
        subject = 'Cambio de estado de publicación'
        message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
        message.content_subtype = 'html'
        message.send()

        # Redirigir a la lista de a publicar
        return redirect('list_a_publicar')
    
    return render(request, 'contenido/dar_nota_form.html', {'contenido': contenido, 'opcion': 'publicar'})

@permission_required('contenido.puede_publicar_rechazar')
def rechazar_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    if request.method == 'POST':
        nota = request.POST.get('nota')
        contenido.nota = nota
        # Cambiar el estado del contenido a "Rechazado"
        contenido.estado = 'Rechazado'
        contenido.save_version(user=request.user)
        content_url = request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
        context = {
            'titulo': contenido.titulo,  
            'nota': contenido.nota,   
            'content_url': content_url, 
        }      
        html_template = 'notificaciones/rechazado.html'
        html_message = render_to_string(html_template, context)
        subject = 'Cambio de estado de publicación'
        message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
        message.content_subtype = 'html'
        message.send()
        return redirect('list_a_publicar')

    return render(request, 'contenido/dar_nota_form.html', {'contenido': contenido, 'opcion': 'rechazar'})

class ContenidoBorradorListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Contenido
    permission_required = 'contenido.add_contenido'
    template_name = 'borrador/borradores_lista.html'
    context_object_name = 'contenidos_borrador'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Borrador').order_by('-fecha')

class ContenidoRechazadoListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Contenido
    permission_required = 'contenido.add_contenido'
    template_name = 'contenido/rechazados_lista.html'
    context_object_name = 'contenidos_rechazados'

    def get_queryset(self):
        # Obtener los contenidos en estado "rechazado" del usuario actual
        return Contenido.objects.filter(user=self.request.user, estado='Rechazado').order_by('-fecha')


def detalle_contenido(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)
    
    if not contenido.is_active:
        return redirect('pagina_no_encontrada')

    if contenido.solo_suscriptores and not request.user.is_authenticated:
        return redirect('error403')
    
    if contenido.estado == 'Publicado':
        contenido.visitas += 1
        contenido.save()

    if request.user.is_authenticated:
        user_likes_contenido = request.user.contenido_likes.filter(id=contenido.id).exists()
        user_dislikes_contenido = request.user.contenido_dislikes.filter(id=contenido.id).exists()
    else:
        user_likes_contenido = False
        user_dislikes_contenido = False
    
    promedio_calificacion = contenido.obtener_promedio_calificacion()
    cantidad_calificaciones = Calificacion.objects.filter(contenido=contenido).count()
    calificacion = None

    if request.user.is_authenticated:
        calificacion = Calificacion.objects.filter(contenido=contenido, usuario=request.user).first()
        if request.method == 'POST':
            
            estrellas = request.POST.get('estrellas')

            if calificacion:
                if estrellas != '0':
                    calificacion.estrellas = estrellas
                    calificacion.save()
                else:
                    calificacion.delete()
            else:
                Calificacion.objects.create(contenido=contenido, usuario=request.user, estrellas=estrellas)
            return redirect('detalle_contenido', pk=pk)
        if calificacion:
            calificacion = calificacion.estrellas

    

    return render(request, 'contenido/contenido_detalle.html', {'contenido': contenido,
    'user_likes_contenido': user_likes_contenido,  'user_dislikes_contenido': user_dislikes_contenido, 
    'promedio_calificacion': promedio_calificacion,
    'calificacion': calificacion,
    'cantidad_calificaciones': cantidad_calificaciones})

def error403(request):
    return render(request, 'error/forbidden.html')

def toggle_like(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)

    if request.user.is_authenticated:
        try:
            # Intenta obtener el like existente del usuario para este contenido
            dislike = Dislike.objects.get(contenido=contenido, user=request.user)
            dislike.delete()  # Elimina el dislike existente     
            messages.success(request, 'DisLike eliminado correctamente.')
        except Dislike.DoesNotExist:
            messages.success(request, 'Dislike eliminado correctamente.')
        try:
            # Intenta obtener el like existente del usuario para este contenido
            like = Like.objects.get(contenido=contenido, user=request.user)
            like.delete()  # Elimina el dislike existente     
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

def toggle_dislike(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    
    if request.user.is_authenticated:
        try:
            # Intenta obtener el like existente del usuario para este contenido
            like = Like.objects.get(contenido=contenido, user=request.user)
            like.delete()  # Elimina el dislike existente     
            messages.success(request, 'Like eliminado correctamente.')
        except Like.DoesNotExist:
            messages.success(request, 'Like eliminado correctamente.')
        try:
            # Intenta obtener el like existente del usuario para este contenido
            dislike = Dislike.objects.get(contenido=contenido, user=request.user)
            dislike.delete()  # Elimina el dislike existente     
            messages.success(request, 'Dislike eliminado correctamente.')
        except Dislike.DoesNotExist:
            # Si el like no existe, créalo (dar like)
            Dislike.objects.create(contenido=contenido, user=request.user)
            messages.success(request, 'Dislike agregado correctamente.')
        # No es necesario incrementar/decrementar el contador de likes aquí
        
       
        return redirect('detalle_contenido', pk=contenido.id)
    else:
        messages.error(request, 'Debes estar autenticado para dar/quitar like.')
        return redirect('detalle_contenido', pk=contenido.id)
    

class EditarContenidoView(UpdateView, PermissionRequiredMixin):
    model = Contenido
    permission_required = 'contenido.change_contenido'
    form_class = ContenidoEditForm
    template_name = 'contenido/contenido_editar.html'
    success_url = reverse_lazy('listar_revisiones')

    def form_valid(self, form):
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=form.instance, image=image)

        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=form.instance, video=video)

        for archivo in self.request.FILES.getlist('archivos'):
            Archivos.objects.create(contenido=form.instance, archivo=archivo)
        
        contenido = form.save(commit=False)
        contenido.save_version(user=self.request.user)

        return redirect(reverse_lazy('listar_revisiones'))
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditarBorradorView(UpdateView):
    model = Contenido
    form_class = BorradorEditForm
    template_name = 'borrador/borrador_editar.html'
    success_url = reverse_lazy('borradores_lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'
        if 'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                form.instance.estado = 'En revisión'
            else:
                form.instance.estado = 'Publicado'
        contenido = form.save(commit=False)
        contenido.save_version(user=self.request.user)
        if  'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
                context = {
                    'titulo': form.instance.titulo,  
                    'content_url': content_url,    
                }      
                html_template = 'notificaciones/en_revision.html'
                html_message = render_to_string(html_template, context)
                subject = 'Cambio de estado de publicación'
                message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
                message.content_subtype = 'html'
                message.send()
            else:
                content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
                context = {'titulo': form.instance.titulo,'content_url': content_url,}      
                html_template = 'notificaciones/publicado_no_moderada.html'
                html_message = render_to_string(html_template, context)
                subject = 'Cambio de estado de publicación'
                message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
                message.content_subtype = 'html'
                message.send()

        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=contenido, image=image)
        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=contenido, video=video)
        for archivo in self.request.FILES.getlist('archivos'):
            Archivos.objects.create(contenido=contenido, archivo=archivo)
        return redirect(reverse_lazy('borradores_lista'))
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class EditarRechazadoView(UpdateView):
    model = Contenido
    form_class = RechazadoEditForm
    template_name = 'contenido/rechazado_editar.html'
    success_url = reverse_lazy('rechazados_lista')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'borradorcito' in self.request.POST:
            form.instance.estado = 'Borrador'
        if 'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                form.instance.estado = 'En revisión'
            else:
                form.instance.estado = 'Publicado'
        contenido = form.save(commit=False)
        contenido.save_version(user=self.request.user)
        if  'crear' in self.request.POST:
            if form.instance.categoria.moderada :
                content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
                context = {
                    'titulo': form.instance.titulo,  
                    'content_url': content_url,    
                }      
                html_template = 'notificaciones/en_revision.html'
                html_message = render_to_string(html_template, context)
                subject = 'Cambio de estado de publicación'
                message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
                message.content_subtype = 'html'
                message.send()
            else:
                content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
                context = {'titulo': form.instance.titulo,'content_url': content_url,}      
                html_template = 'notificaciones/publicado_no_moderada.html'
                html_message = render_to_string(html_template, context)
                subject = 'Cambio de estado de publicación'
                message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
                message.content_subtype = 'html'
                message.send()
        # Busca el nombre 'borradorcito' entre los atributos del elemento para distinguir el boton
        if 'borradorcito' in self.request.POST:
            content_url = self.request.build_absolute_uri(reverse('detalle_contenido', args=[contenido.pk]))
            context = {
                    'titulo': form.instance.titulo,      
                    'content_url': content_url,
                }      
            html_template = 'notificaciones/borrador.html'
            html_message = render_to_string(html_template, context)
            subject = 'Cambio de estado de publicación'
            message=EmailMessage(subject, html_message, 'cmsis2eq01@gmail.com', [contenido.user.email])
            message.content_subtype = 'html'
            message.send()
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(contenido=contenido, image=image)
        for video in self.request.FILES.getlist('videos'):
            Video.objects.create(contenido=contenido, video=video)
        for archivo in self.request.FILES.getlist('archivos'):
            Archivos.objects.create(contenido=contenido, archivo=archivo)
        return redirect(reverse_lazy('rechazados_lista'))
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

def detalle_autor(request, pk):
    # Obtiene el usuario (autor) por su clave primaria (pk)
    autor = get_object_or_404(User, pk=pk)

    # Obtiene los contenidos relacionados al autor
    contenidos = Contenido.objects.filter(user=autor,estado='Publicado', is_active=True).order_by('-fecha')

    # Renderiza el template para mostrar los detalles del autor y sus contenidos
    return render(request, 'autor/contenidos_autor.html', {'autor': autor, 'contenidos': contenidos})

@permission_required('contenido.ver_kanban')
def kanban_view(request):
    contexto={'contenidos': Contenido.objects.filter(user=request.user).order_by('-fecha')}
    return render(request, 'kanban.html', contexto)

@permission_required('contenido.ver_todos_kanban')
def all_kanban_view(request):
    contexto={'contenidos': Contenido.objects.all().order_by('-fecha')}
    return render(request, 'kanban.html', contexto)

def delete_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    if request.user == image.contenido.user:
        content_pk = image.contenido.pk
        estado = image.contenido.estado 
        image.delete()
        print(estado)
        if estado == 'Borrador':
            edit_url = 'editar-borrador'
        elif estado == 'Publicado' or 'En revisión':
            edit_url = 'editar-contenido'
        else:
            pass
        return redirect(edit_url, pk=content_pk)
    
def delete_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    if request.user == video.contenido.user:
        content_pk = video.contenido.pk
        estado = video.contenido.estado
        video.delete()
        if estado == 'Borrador':
            edit_url = 'editar-borrador'
        elif estado == 'Publicado' or 'En revisión':
            edit_url = 'editar-contenido'
        elif estado == 'Rechazado':
            edit_url = 'editar-rechazado'
        else:
            pass
        return redirect(edit_url, pk=content_pk)
    
def delete_archivo(request, archivo_id):
    archivo = get_object_or_404(Archivos, pk=archivo_id)
    if request.user == archivo.contenido.user:
        content_pk = archivo.contenido.pk
        estado = archivo.contenido.estado
        archivo.delete()
        if estado == 'Borrador':
            edit_url = 'editar-borrador'
        elif estado == 'Publicado' or estado == 'En revisión':  # Fix the 'or' condition
            edit_url = 'editar-contenido'
        elif estado == 'Rechazado':
            edit_url = 'editar-rechazado'
        else:
            pass
        return redirect(edit_url, pk=content_pk)


class ContenidoVersionListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = VersionContenido
    template_name = 'version/historial_lista.html'
    permission_required = 'contenido.add_contenido'
    context_object_name = 'version_contenidos'

    def get_queryset(self, **kwargs):
        contenido_id = self.kwargs.get('contenido_id')
        if contenido_id:
            micontenido = Contenido.objects.filter(user = self.request.user, id=contenido_id)
            return VersionContenido.objects.filter(contenido__in = micontenido).order_by('-contenido_id', 'version')
        else:
            micontenido = Contenido.objects.filter(user = self.request.user)
            return micontenido

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contenido_id = self.kwargs.get('contenido_id')
        print(contenido_id)
        if not contenido_id:
            context['modo'] = 'contenidos'
        else:
            context['modo'] = 'versiones'
        return context
def editar_version(request, version_id):
    version = get_object_or_404(VersionContenido, pk=version_id)
    
    if request.method == 'POST':
        form = VersionContenidoEditForm(request.POST, instance=version, user_request=request.user)
        if form.is_valid():
            nueva_version = form.save(commit=False)

        if version.contenido.estado == 'Borrador':
            for video in request.FILES.getlist('videos'):
                Video.objects.create(contenido=nueva_version.contenido, video=video)
            for archivo in request.FILES.getlist('archivos'):
                Archivos.objects.create(contenido=nueva_version.contenido, archivo=archivo)
            contenido = version.contenido
            contenido.titulo = nueva_version.titulo
            contenido.resumen = nueva_version.resumen
            contenido.descripcion = nueva_version.descripcion
            contenido.categoria = nueva_version.categoria
            contenido.estado = nueva_version.estado
            contenido.nota = nueva_version.nota
            contenido.save_version(user=request.user)
            return redirect(reverse_lazy('contenido-version'))  # Redirigir a la lista de versiones
    else:
        form = VersionContenidoEditForm(instance=version, user_request=request.user)
    
    return render(request, 'version/version_editar.html', {'form': form, 'version': version})
    
class ContenidoHistorialListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = VersionContenido
    template_name = 'version/historial_lista.html'
    permission_required = 'contenido.ver_historial'
    context_object_name = 'version_contenidos'

    def get_queryset(self):
        # Obtener los contenidos en estado "borrador" del usuario actual
        return VersionContenido.objects.all().order_by('-fecha_modificacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modo'] = 'historial'
        return context
    
def detalle_historial(request, version_id):
    version = get_object_or_404(VersionContenido, pk=version_id)
    return render(request, 'version/historial_vista.html', {'version': version})

def toggle_favorito(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.user.is_authenticated:
        try:
            favorito = Favoritos.objects.get(categoria=categoria, user=request.user)
            favorito.delete()
        except Favoritos.DoesNotExist:
            Favoritos.objects.create(categoria=categoria, user=request.user)
    else:
        messages.error(request, 'Debes estar autenticado para seguir una categoria.')
        return redirect('mostrar_contenidos', pk=categoria.id)
    return redirect('mostrar_contenidos', pk=categoria.id)

def compartir_contenido(request, contenido_id):
    contenido = get_object_or_404(Contenido, pk=contenido_id)
    contenido.compartidos += 1
    contenido.save()
    response_data = {'message': 'URL copiado al portapapeles'}
    return JsonResponse(response_data)

def generate_qr_code(request):
    # Obtiene la URL actual
    current_url = request.META['HTTP_REFERER']
    print(current_url)
    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agrega la URL actual al objeto QRCode
    qr.add_data(current_url)
    qr.make(fit=True)

    # Crea una imagen del código QR
    img = qr.make_image(fill_color="black", back_color="white")

    # Guarda la imagen en un BytesIO
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    image_file = File(buffer)

    # Renderiza la imagen en la respuesta HTTP
    return HttpResponse(image_file, content_type="image/png")

@login_required
def confirmar_desactivacion(request, pk):
    contenido = get_object_or_404(Contenido, pk=pk)

    if request.method == 'POST':
        # Si el usuario confirma la desactivación
        contenido.is_active = False
        contenido.save()

        return redirect('index')  # Redirigir a donde desees después de la desactivación

    return render(request, 'contenido/confirmar_desactivacion.html', {'contenido': contenido})

@login_required
def estadisticas(request):
    contenidos = Contenido.objects.filter(estado='Publicado', is_active=True).order_by('-fecha')
    return render(request, 'contenido/estadisticas.html', {'contenidos': contenidos})