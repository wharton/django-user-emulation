from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.http import is_safe_url

from django_user_emulation.signals import emulation_started, emulation_ended


def end_emulation(request):

    logged_in_user = None
    emulated_user = None
    emulated_user = request.user
    logged_in_user = get_object_or_404(get_user_model(), pk=request.session['logged_in_user'])
    logged_in_user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, logged_in_user)
    request.session.pop('is_emulating', None)
    request.session.modified = True
    emulation_ended.send(sender=None, logged_in_user_id=logged_in_user.pk,
                         emulated_user_id=emulated_user.pk, request=request)
    return redirect_to_next(request)


def login_user(request, emulated_user):
    logged_in_user = request.user

    emulated_user.backend = settings.AUTHENTICATION_BACKENDS[0]

    # we don't want login to trigger update of last login date
    user_logged_in.disconnect(update_last_login)

    # Actually log user in
    login(request, emulated_user)

    # turn back on login signal to update last login
    user_logged_in.connect(update_last_login)

    emulation_started.send(sender=None, logged_in_user_id=logged_in_user.pk,
                           emulated_user_id=emulated_user.pk, request=request)  # Send official, documented signal
    request.session['logged_in_user'] = logged_in_user.pk
    request.session['is_emulating'] = True
    request.session.modified = True
    return redirect_to_next(request)


def redirect_to_next(request):
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    if not is_safe_url(redirect_to):
        redirect_to = '/'
    return HttpResponseRedirect(redirect_to)
