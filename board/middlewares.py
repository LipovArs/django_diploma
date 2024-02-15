from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

import datetime


AFK_LOG_OUT_TIME = 60

class LogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_anonymous and not request.user.is_superuser:
            now = datetime.datetime.now()
            last_action_not_decoded = request.session.get('last_action')
            if last_action_not_decoded:
                last_action = datetime.datetime.strptime(last_action_not_decoded, "%H-%M-%S %d/%m/%y")
                if (now - last_action).seconds > AFK_LOG_OUT_TIME:
                    try:
                        request.user.auth_token.delete()
                    except:
                        pass
                    try:
                        logout(request)
                    except:
                        pass
                try:
                    request.user.auth_token
                except:
                    logout(request)
            request.session['last_action'] = datetime.datetime.now().strftime("%H-%M-%S %d/%m/%y")