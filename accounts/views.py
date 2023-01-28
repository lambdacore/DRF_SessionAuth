from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import BaseUser
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import permissions, viewsets, mixins
from django.contrib import auth
from rest_framework.response import Response
from .serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.shortcuts import render

class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })


@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class AccountsViewSet(viewsets.ViewSet,mixins.ListModelMixin):

    def create (self, request, format=None):
        #permission_classes = (permissions.AllowAny,)
        data = self.request.data

        username = data['username']
        password = data['password']
        re_password  = data['re_password']

        try:
            if password == re_password:
                if BaseUser.objects.filter(username=username).exists():
                    return Response({ 'error': 'Username already exists' })
                else:
                    if len(password) < 6:
                        return Response({ 'error': 'Password must be at least 6 characters' })
                    else:
                        user = BaseUser.objects.create_user(username=username, password=password)

                        user = BaseUser.objects.get(id=user.id)
                        return Response({ 'success': 'User created successfully' })
            else:
                return Response({ 'error': 'Passwords do not match' })
        except:
                return Response({ 'error': 'Something went wrong when registering account' })
    def delete(self, request, format=None):
        user = self.request.user
        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                User.objects.filter(id=user.id).delete()
            else:
                return Response({'isAuthenticated': 'error'})
            return Response({ 'success': 'User deleted successfully' })
        except:
            return Response({ 'error': 'Something went wrong when trying to delete user' })
    def retrieve(self,request,pk=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                queryset = BaseUser.objects.all()
                user_data = get_object_or_404(queryset, pk = pk)
                serializer = UserSerializer(user_data)
                return Response(serializer.data)
                #return Response({'isAuthenticated': 'success'})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})

@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return Response({ 'success': 'User authenticated' })
            else:
                return Response({ 'error': 'Error Authenticating' })
        except:
            return Response({ 'error': 'Something went wrong when logging in' })

@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': 'Loggout Out' })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })


