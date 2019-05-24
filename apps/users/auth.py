from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import Token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN")
        if not token:
            raise exceptions.AuthenticationFailed('请传入token值')
        else:
            token_obj = Token.objects.filter(token=token).first()
            if not token_obj:
                raise exceptions.AuthenticationFailed('token验证失败，请检查')
            else:
                update_time = token_obj.update_time
                import datetime
                update_time = update_time.strftime('%Y-%m-%d %H:%M:%S')
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                delta = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
                    update_time, '%Y-%m-%d %H:%M:%S')
                import web_auto.settings as setting
                if delta.seconds > setting.TOKEN_EFFETIVE_TIME:
                    raise exceptions.AuthenticationFailed('token失效')
                else:
                    return token_obj.user, token_obj.token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass
