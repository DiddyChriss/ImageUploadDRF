from django.urls import path, include


from .views import ImageAPIView



app_name = 'ImageDRF'
urlpatterns = [
    path('', ImageAPIView.as_view({'get':'list'}), name='ImageDRFapi'),
]
