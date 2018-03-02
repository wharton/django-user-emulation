from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model, get_user
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from django_user_emulation.views import EmulateView, EmulateEndView


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class EmulationViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.client.login(username=self.superuser.username, password='you shall not pass')
        client_user = get_user(self.client)
        self.assertEqual(client_user, self.superuser)
        self.assertTrue(client_user.is_authenticated())

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the gray')
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'you shall not pass')

    def test_integration(self):
        response = self.client.post(reverse('django_user_emulation:emulate-start'), {'emulate_user_id': self.user.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        response = self.client.post(reverse('django_user_emulation:emulate-end'), {'next': "/blah"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/blah")

    def test_EmulationView_get(self):
        request = self.factory.get('/blah', {'emulate_user_id': self.user.pk})
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        view = setup_view(EmulateView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_EmulationView_post(self):
        request = self.factory.post('/blah', {'emulate_user_id': self.user.pk})
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        view = setup_view(EmulateView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_EmulationView_get_no_userid(self):
        request = self.factory.get('/blah')
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        view = setup_view(EmulateView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            b"int() argument must be a string, a bytes-like object or a number, not 'NoneType'", response.content)

    def test_EmulationView_get_invalid_userid(self):
        request = self.factory.get('/blah', {'emulate_user_id': 'not a number'})
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        view = setup_view(EmulateView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(b"Incorrect id value requested.", response.content)

    def test_EmulationView_get_bad_userid(self):
        request = self.factory.get('/blah', {'emulate_user_id': 123456})
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        view = setup_view(EmulateView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(b"No User matches the given query.", response.content)

    def test_EmulationEndView_get(self):
        request = self.factory.get('/blah')
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['logged_in_user'] = self.superuser.pk
        request.session.save()
        view = setup_view(EmulateEndView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 302)

    def test_EmulationEndView_post(self):
        request = self.factory.post('/blah')
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['logged_in_user'] = self.superuser.pk
        request.session.save()
        view = setup_view(EmulateEndView(), request)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        self.assertEqual(response.status_code, 302)
