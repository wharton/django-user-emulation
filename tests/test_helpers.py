from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware

from django_user_emulation.helpers import end_emulation, login_user, redirect_to_next


class TestDjango_user_emulation(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the gray')
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'fireworks')

    def test_end_emulation(self):
        request = self.factory.get('/blah')
        request.user = self.user
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['logged_in_user'] = self.superuser.pk
        request.session.save()

        result = end_emulation(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.url, "/")

    def test_login_user(self):
        request = self.factory.get('/blah')
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        result = login_user(request, self.user)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.url, "/")

    def test_redirect_to_next(self):
        request = self.factory.get('/blah', {'next': '/blahurl'})
        result = redirect_to_next(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.url, "/blahurl")

    def test_redirect_to_next_invalid_next(self):
        request = self.factory.get('/blah', {'next': '///unsafeurl'})
        result = redirect_to_next(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.url, "/")

    def test_redirect_to_next_no_next(self):
        request = self.factory.get('/blah')
        result = redirect_to_next(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.url, "/")

    def test_redirect_to_next_none_next(self):
        # post/get request turns next None to text 'None' which is apparently valid
        request = self.factory.get('/blah', {'next': None})
        result = redirect_to_next(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result.url, "None")

    def test_redirect_to_next_no_next_param_use_alias(self):
        request = self.factory.get('/yum')
        request.META['SCRIPT_NAME'] = '/apache'
        self.assertEqual(redirect_to_next(request).url, '/apache')

    def tearDown(self):
        pass
