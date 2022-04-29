from rest_framework.generics import CreateAPIView
from accounts.serializers.register_serializer import RegisterSerializer

class Register(CreateAPIView):
    serializer_class = RegisterSerializer
