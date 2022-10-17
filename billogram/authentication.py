import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import exceptions
from rest_framework.authentication import (BaseAuthentication,
                                           get_authorization_header)
from billogram.discountservice.models import Brand, User



class JSONWebTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        token = get_authorization_header(request).decode().split()

        if 'Bearer' not in token:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Bearer String Not Set'
            })
        try:
            payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload['uid']).first(
            ) or Brand.objects.filter(id=payload['uid']).first()
        except (jwt.DecodeError, IndexError, KeyError):
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Token has expired'
            })

        if not user:
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })

        if not user.is_active:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'User has not been verified'
            })

        return (user, payload)

#Giving identity and permission based on authenticated user decoded from Token in request body...
class AllowAnyUser(BaseAuthentication):
    def authenticate(self, request):
        # self.payload = {}
        try:
            token = get_authorization_header(request).decode().split()
            if 'Bearer' in token:
                self.payload = jwt.decode(token[1],
                                          settings.SECRET_KEY,
                                          algorithms=['HS256'])
        except (jwt.DecodeError, KeyError, IndexError):
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Token has expired'
            })
        payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.filter(id=self.payload.get('uid')).first()or Brand.objects.filter(id=payload['uid']).first()
        if not user:
            return (AnonymousUser, None)

        if not user.is_active:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'User has not been verified'
            })

        return (user, payload)




#Giving identity and permission based on authenticated user decoded from Token in request body...

class BrandOnlyAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    def authenticate(self, request):
        token = get_authorization_header(request).decode().split()

        if 'Bearer' not in token:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Bearer String Not Set'
            })
        try:
            payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
            user = Brand.objects.filter(id=payload['uid']).first()

        except (jwt.DecodeError, IndexError, KeyError):
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Token has expired'
            })

        if not user:
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })

        if not user.is_active:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'User has not been verified'
            })

        return (user, payload)

#Giving identity and permission based on authenticated user decoded from Token in request body...

class AllUsersAuthentication(BaseAuthentication):
    keyword = 'Bearer'
    def authenticate(self, request):
        token = get_authorization_header(request).decode().split()

        if 'Bearer' not in token:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Bearer String Not Set'
            })
        try:
            payload = jwt.decode(token[1], settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.filter(id=payload['uid']).first(
            ) or Brand.objects.filter(id=payload['uid']).first()
        except (jwt.DecodeError, IndexError, KeyError):
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'Token has expired'
            })

        if not user:
            raise exceptions.AuthenticationFailed({
                'error':
                'Authentication Failed',
                'message':
                'Cannot validate your access credentials'
            })

        if not user.is_active:
            raise exceptions.AuthenticationFailed({
                'error': 'Authentication Failed',
                'message': 'User has not been verified'
            })

        return (user, payload)
