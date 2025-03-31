from django.conf.urls.static import static
from django.urls import path

from website import settings
from . import views

urlpatterns = [
    path('', views.show_pages, name='website'),
    path('page=<int:page>/', views.show_pages, name='pages'),
]
