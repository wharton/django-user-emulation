from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import FormView, View

from .forms import EmulationForm


class EmulateView(PermissionRequiredMixin, FormView):
    permission_required = 'is_superuser'
    template_name = 'speaker/emulate.html'
    form_class = EmulationForm
    success_url = reverse_lazy('home')


class AutocompleteView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_queryset())

    def get_queryset(self):
        # get the term from the url, depending on which autocomplete is used....
        term = self.request.GET.get('term', self.request.GET.get('q', ''))

        qo_filter = Q()
        queryset = None

        if term != '':
            qo_filter |= Q(user__username__icontains=term)
            qo_filter |= Q(user__email__icontains=term)
            qo_filter |= Q(user__first_name__icontains=term)
            qo_filter |= Q(user__last_name__icontains=term)
            queryset = get_user_model().objects.filter(qo_filter)

        results = []
        for user in queryset:
            name_json = {}
            name_json['id'] = user.id
            name_json['label'] = "{}, {}: {}".format(
                user.last_name, user.first_name, user.username)
            name_json['value'] = user.name
            results.append(name_json)
        return results
