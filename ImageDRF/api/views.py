from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response

from ImageDRF.models import Image, Account, User

from .serializers import UserSerializer

class ImageAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    queryset = Image.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            user = User.objects.get(userUser=request.user)
        except:
            account = Account.objects.get(name='Basic')
            user = User.objects.create(userUser=request.user, account=account)

        queryset = queryset.filter(user=user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


    def perform_create(self, serializer):
        userUser = User.objects.get(userUser=self.request.user)
        return serializer.save(user=userUser)

    def post(self, request):
        return self.create(request)

