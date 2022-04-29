from rest_framework.generics import RetrieveAPIView
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from accounts.serializers.profile import GetProfileSerializer,EditProfileSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
import os

class ProfileView(RetrieveAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticated,]

    # Get Request
    def get(self, request, *args, **kwargs):
        self.serializer_class = GetProfileSerializer
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    # Put Request
    def put(self, request, *args, **kwargs):
        self.serializer_class = EditProfileSerializer
        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        self.serializer_class = EditProfileSerializer
        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        password = serializer.pop_password()
        if serializer.check_avatar():
            user_db = User.objects.get(id=user.id)
            avatar_url = user_db.avatar.url
            if avatar_url != "/media/avatars/user-default.jpeg":
                os.remove(user_db.avatar.path)
        self.perform_update(serializer)
        if password != '':
            user.set_password(password)
            user.save()

        if getattr(user, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            user._prefetched_objects_cache = {}

        return Response(HTTP_200_OK)
