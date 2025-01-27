from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth.models import Group


@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({"message": "Hello, World!"})


class GroupsListView(APIView):
    def get(self, request: Request) -> Response:
        groups = Group.objects.all()
        data = [group.name for group in groups]
        return Response({"groups": data})

    def post(self, request: Request) -> Response:
        user = request.user
        return Response({"message": f"Hello from {user.username}!"})
