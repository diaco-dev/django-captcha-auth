# core/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            raise AuthenticationFailed('Authorization token is missing')

        try:
            # Strip "Bearer" if it exists
            if token.startswith("Bearer "):
                token = token[7:]

            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user = get_user_model().objects.get(pk=payload['user_id'])
        if user is None:
            raise AuthenticationFailed('User not found')

        return (user, None)  # Return the user and None for auth header


