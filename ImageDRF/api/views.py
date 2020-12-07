from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response

from ImageDRF.models import Image, Plan, AccountUser

from .serializers import UserSerializer

class ImageAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    queryset = Image.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = AccountUser.objects.get(user_account=request.user)
        queryset = queryset.filter(user=user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


    def perform_create(self, serializer):
        user_account = AccountUser.objects.get(user_account=self.request.user)
        return serializer.save(user=user_account)

    def post(self, request):
        return self.create(request)

