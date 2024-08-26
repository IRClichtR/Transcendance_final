from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden

def CustomMiddleware(get_response):
    def middleware(request):
        # added 'and not request.user.is_authenticated' in condition.
        # because when we login from POST (without 42API) we don't have access_token AND we have /app in path
        # so everytime we wanted to login, we were redirect in login instead of /app
        # i added not is.authenticated because it's an other condition for getting the right redirection
        should_redirect = 'access_token' not in request.session and request.path.startswith("/app/") and not request.user.is_authenticated
        if should_redirect:
            return redirect(reverse('login'))

        response = get_response(request)
        return response

    return middleware

# class RestrictUserAccessMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == '/user/':
#             return HttpResponseForbidden("Access denied")
#         response = self.get_response(request)
#         return response