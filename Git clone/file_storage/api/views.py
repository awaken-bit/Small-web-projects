from main.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers


class SearchRepositorys(APIView):
    def post(self, request):
        speks = request.data
        try:
            last_repository = Repository.objects.get(id=int(speks['id']))

            repositorys = Repository.objects.select_related('owner') \
            .order_by('-changed_at').filter(name__icontains=speks['name'], changed_at__lt=last_repository.changed_at, is_private=False)[:5]
        except:
            return Response({'messeng': 'Ошибка в форамате данных.'})

        serializer = serializers.RepositorySerializer(repositorys, many=True)
        return Response({'messeng':serializer.data})