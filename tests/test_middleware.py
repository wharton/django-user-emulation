from django.test import SimpleTestCase, TestCase, RequestFactory, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from mock import patch, Mock

from django_user_emulation.middleware import EmulationRemoteUserMiddleware


def dummy_request(request):
    return request.META.get("REMOTE_USER", None)


class EmulationMiddlewareMockTests(SimpleTestCase):
    @patch('django_user_emulation.middleware.EmulationRemoteUserMiddleware')
    def test_init(self, my_middleware_mock):
        my_middleware = EmulationRemoteUserMiddleware('response')
        assert(my_middleware.get_response) == 'response'

    def test_mymiddleware(self):
        request = Mock()
        request.user = AnonymousUser()
        request.user.username = "testuser"
        request.META = {
            "REMOTE_USER": "blah",
        }
        request.path = '/testURL/'
        request.session = {}
        my_middleware = EmulationRemoteUserMiddleware(Mock())
        # CALL MIDDLEWARE ON REQUEST HERE
        my_middleware(request)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertEqual(request.META["REMOTE_USER"], "blah")
        self.assertFalse(request.user.is_authenticated)
        self.assertEqual(request.user.username, "testuser")


class EmulationMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username=self.superuser.username,
                          password='You shall not pass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/blah')
        self.request.session = {}
        self.middleware = EmulationRemoteUserMiddleware(dummy_request)

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the gray')
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'You shall not pass')

    def test_requestProcessing(self):
        self.assertIsNone(self.middleware(self.request))
        self.assertFalse("REMOTE_USER" in self.request.META)

    def test_requestProcessing_anonymous_user(self):
        request = self.request
        request.user = AnonymousUser()
        request.META["REMOTE_USER"] = self.user.username
        request.session['is_emulating'] = True
        self.assertEqual(self.middleware(request), self.user.username)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertFalse(request.user.is_authenticated)
        self.assertEqual(request.META["REMOTE_USER"], self.user.username)

    def test_requestProcessing_no_user(self):
        request = self.request
        request.META["REMOTE_USER"] = self.user.username
        request.session['is_emulating'] = True
        self.assertEqual(self.middleware(request), self.user.username)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertFalse(hasattr(request, 'user'))
        self.assertEqual(request.META["REMOTE_USER"], self.user.username)

    def test_requestProcessing_emulated(self):
        request = self.request
        request.user = self.superuser
        request.META["REMOTE_USER"] = self.user.username
        print(request.META["REMOTE_USER"])
        request.session['is_emulating'] = True
        self.assertEqual(self.middleware(request), self.user.username)
        print(request.META["REMOTE_USER"])
        self.assertTrue(request.META["REMOTE_USER"])
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.META["REMOTE_USER"], self.user.username)

    def test_requestProcessing_emulate_self(self):
        request = self.request
        request.user = self.superuser
        request.META["REMOTE_USER"] = self.superuser.username
        request.session['is_emulating'] = True
        self.assertEqual(self.middleware(request), self.superuser.username)
        self.assertTrue(request.META["REMOTE_USER"])
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.META["REMOTE_USER"], self.superuser.username)

    def test_authenticate(self):
        self.assertIsNone(self.middleware.authenticate(self.request))
