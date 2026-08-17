from django.urls import path
from . import views

app_name = 'trgovina_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('oglas/<int:oglas_id>', views.oglas_podrobnosti, name='oglas_podrobnosti'),
    path('najnovejsi/<int:stevilo>', views.oglas_najnovejsi, name='oglas_najnovejsi'),
    path('oglas_poisci', views.oglas_poisci, name='oglas_poisci'),
    path('oglas_dodaj', views.oglas_dodaj, name='oglas_dodaj'),
    path('oglas_uredi/<int:oglas_id>', views.oglas_uredi, name='oglas_uredi'),
    path('kupi', views.oglas_kupi, name='oglas_kupi'),
]
