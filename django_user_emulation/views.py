from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic import View

from django_user_emulation.helpers import login_user
from django_user_emulation.helpers import end_emulation


class EmulateView(PermissionRequiredMixin, View):
    permission_required = 'is_superuser'

    def get(self, request, format=None):
        user_id = request.GET.get('emulateUserId', None)
        return self.handle_emulate(request=request, user_id=user_id)

    def post(self, request, format=None):
        user_id = request.POST.get('emulateUserId', None)
        return self.handle_emulate(request=request, user_id=user_id)

    def handle_emulate(self, request, user_id):
        try:
            user_id = int(user_id)
        except ValueError:
            return HttpResponseBadRequest('Incorrect id value requested.')
        user = get_object_or_404(get_user_model(), pk=user_id)
        return login_user(request, user)


class EmulateEndView(View):

    def get(self, request, format=None):
        return self.handle_emulate(request=request)

    def post(self, request, format=None):
        return self.handle_emulate(request=request)

    def handle_emulate(self, request):
        return end_emulation(request)
