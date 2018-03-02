class emulationRemoteUserMiddleware(object):
    """
    Middleware for emulation RemoteUser. One must place this middleware between
    'django.contrib.auth.middleware.AuthenticationMiddleware' and
    'django.contrib.auth.middleware.RemoteUserMiddleware' in MIDDLEWARE_CLASSES

    Just makes remote user same as emulated_user
    """
    header = "REMOTE_USER"

    def process_request(self, request):
        is_emulated_user = request.session.get('is_emulating', False)
        remote_username = request.META.get(self.header, None)
        if not is_emulated_user or not remote_username:
            return
        # Ok, we emulated_user and remote. Just assign emulated_user user to remote
        if request.user.is_authenticated():
            username = request.user.get_username()
            if username != remote_username:
                request.META[self.header] = username

    def authenticate(self, *args, **kwargs):
        return None
