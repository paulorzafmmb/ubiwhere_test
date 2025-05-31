# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-31 00:35:49
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 00:43:20

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AuthToken


class SensorTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return None

        token = auth.split(" ")[1]
        try:
            auth_token = AuthToken.objects.get(token=token)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        return (auth_token, None)