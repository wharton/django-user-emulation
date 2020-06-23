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
        if not is_emulated_user or not remote_username or not hasattr(request, 'user') or not request.user.is_authenticated:
            return self.get_response(request)
        # User is logged in, we are emulating and we have a remote username, lets set remote_user to username for emulation
        username = request.user.get_username()
        if username != remote_username:
            request.META[self.header] = username
        return self.get_response(request)

    def authenticate(self, *args, **kwargs):
        return None
