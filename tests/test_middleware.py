from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser 

from django_user_emulation.middleware import EmulationRemoteUserMiddleware


class AnalyiticsMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username=self.superuser.username, password='You shall not pass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/blah')
        self.request.user = self.user
        self.request.session = {}
        self.middleware = EmulationRemoteUserMiddleware()

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the gray')
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'You shall not pass')

    def test_requestProcessing(self):
        self.assertIsNone(self.middleware.process_request(self.request))
        self.assertFalse("REMOTE_USER" in self.request.META)

    def test_requestProcessing_anonymous_user(self):
        request = self.request
        request.user = AnonymousUser()
        request.META["REMOTE_USER"] = self.user.username
        session = self.client.session
        session['is_emulating'] = True
        session.save()
        request.session = session
        self.assertIsNone(self.middleware.process_request(request))
        self.assertTrue("REMOTE_USER" in self.request.META)

    def test_requestProcessing_emulated(self):
        request = self.request
        request.META["REMOTE_USER"] = self.user.username
        session = self.client.session
        session['is_emulating'] = True
        session.save()
        request.session = session
        self.assertIsNone(self.middleware.process_request(request))
        self.assertTrue(request.META["REMOTE_USER"])

    def test_requestProcessing_emulate_self(self):
        request = self.request
        request.META["REMOTE_USER"] = self.superuser.username
        session = self.client.session
        session['is_emulating'] = True
        session.save()
        request.session = session
        self.assertIsNone(self.middleware.process_request(request))
        self.assertTrue(request.META["REMOTE_USER"])

    def test_authenticate(self):
        self.assertIsNone(self.middleware.authenticate(self.request))
