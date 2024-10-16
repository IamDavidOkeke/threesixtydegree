from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

AUTH_EXEMPT_ROUTES = ('register', 'login', 'home')

class LoginRequiredMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        current_route_name = resolve(request.path_info).url_name

        if  request.user.is_authenticated:
            return

        if current_route_name in AUTH_EXEMPT_ROUTES:
            return


        return login_required(view_func)(request, *view_args, **view_kwargs)