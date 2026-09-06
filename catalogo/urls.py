from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:producto_id>/', views.detalle, name='detalle'),
]