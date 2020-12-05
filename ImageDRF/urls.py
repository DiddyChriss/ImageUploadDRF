from django.urls import path
from .views import basedview

app_name = 'ImageDRF'
urlpatterns = [
    path('', basedview, name='main'),
]