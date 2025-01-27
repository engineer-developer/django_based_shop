from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.models import Group

from .serializers import GroupSerializer


@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello, World!"})


# Implement "APIView"
# class GroupsListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         # data = [group.name for group in groups]
#         # return Response({"groups": data})
#
#         serialized = GroupSerializer(groups, many=True)
#         return Response({"groups": serialized.data})


# Implement "GenericAPIView" and "ListModelMixin"
# class GroupsListView(ListModelMixin, GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)

