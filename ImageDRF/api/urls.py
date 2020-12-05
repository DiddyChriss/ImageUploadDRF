from django.urls import path, include

from .views import ImageAPIView

from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'list_of_images', ImageAPIView)


app_name = 'ImageDRF'
urlpatterns = [
    path('', include(router.urls)),
]
