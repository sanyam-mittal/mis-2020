from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions, generics, viewsets, authentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . import models, serializers


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'full_name': user.get_full_name(),
        }
        try:
            response['designation'] = user.profile.designation
        except:
            pass
        return Response(response)


class All_ZM_APIViewset(generics.ListAPIView):
    queryset = models.Profile.zm_objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)


class All_PM_APIViewset(generics.ListAPIView):
    queryset = models.Profile.pm_objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)


class All_PC_APIViewset(generics.ListAPIView):
    queryset = models.Profile.pc_objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)


class All_MIS_APIViewset(generics.ListAPIView):
    queryset = models.Profile.mis_objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAuthenticated,)


class NotificationViewset(viewsets.ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = models.Notification.objects.filter(to_user=user)
        return queryset