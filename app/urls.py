from django.urls import path
from . import views
app_name = 'tv-shows'
urlpatterns = [
    path('', views.redirigir, name="redirigir"),
    path('shows/', views.index, name='shows'),
    path('shows/new', views.newtvshow, name='agregar'),
    path('shows/create', views.createtvshow, name='crear'),
    path('shows/<int:id>', views.details, name='detalles'),
    path('shows/<int:id>/edit', views.edit, name='editar'),
    path('shows/<int:id>/update', views.update, name='actualizar'),
    path('shows/<int:id>/destroy', views.destroy, name='eliminar'),
]
