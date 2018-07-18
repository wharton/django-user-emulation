class EmulationRemoteUserMiddleware(object):
    """
    Middleware for emulation RemoteUser. One must place this middleware between
    'django.contrib.auth.middleware.AuthenticationMiddleware' and
    'django.contrib.auth.middleware.RemoteUserMiddleware' in MIDDLEWARE

    Just makes remote user same as emulated_user
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.header = "REMOTE_USER"

    def __call__(self, request):
        is_emulated_user = request.session.get('is_emulating', False)
        remote_username = request.META.get(self.header, None)
        if not is_emulated_user or not remote_username or not hasattr(request, 'user'):
            return self.get_response(request)
        # Ok, we emulated_user and remote. Just assign emulated_user user to remote
        if request.user.is_authenticated:
            username = request.user.get_username()
            if username != remote_username:
                request.META[self.header] = username
                print(request.META["REMOTE_USER"])

        response = self.get_response(request)
        return response

    def authenticate(self, *args, **kwargs):
        return None
