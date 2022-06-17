
from django.http import request, Http404, HttpResponse, JsonResponse
from rest_framework import viewsets, generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import *
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from .serializer import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsClientUser, IsPhotographerUser
from rest_framework.permissions import AllowAny


class Get_all_photographers(generics.ListCreateAPIView):
    queryset = Photographer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PhotographerSerializer


class Get_all_clients(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClientSerializer


class Get_all_users(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class AllUsers(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class AllPhotographers(viewsets.ModelViewSet):
    serializer_class = PhotographerSerializer
    queryset = Photographer.objects.all()


class AllClients(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class AllEvents(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class AllPhotos(viewsets.ModelViewSet):
    serializer_class = PhotosSerializer
    queryset = Photos.objects.all()


class AllFeedback(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
class AllPortfolios(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()

class ClientSignupView(generics.CreateAPIView):
    queryset = Client.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ClientSignupSerializer


class PhotographerSignupView(generics.CreateAPIView):
    queryset = Photographer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PhotographerSignupSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_client': user.is_client,
            'is_photographer': user.is_photographer
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & IsClientUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PhotographerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & IsPhotographerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class EventView(APIView):
    def get_all(self, request, format=None):
        all = Event.objects.all()
        serializers = EventSerializer(all, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = EventSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_event(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Http404

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        event = self.get_event(pk)
        serializers = EventSerializer(event)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        event = self.get_event(pk)
        serializers = EventSerializer(event, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_event(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotosList(APIView):
    def get(self, request, format=None):
        photos = Photos.objects.all()
        serializers = PhotosSerializer(photos, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = PhotosSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
