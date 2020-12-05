from django.urls import path, include

from rest_framework import routers

from .views import ImageAPIView


router = routers.DefaultRouter()
router.register(r'list_of_images', ImageAPIView)


app_name = 'ImageDRF'
urlpatterns = [
    # path('', include(router.urls)),
    path('', ImageAPIView.as_view({'get':'list'}), name='ImageDRFapi'),
]
