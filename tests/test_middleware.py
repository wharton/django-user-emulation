from django.http import HttpResponse
from django.test import SimpleTestCase, TestCase, RequestFactory, Client, override_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from unittest.mock import patch, Mock, MagicMock


from django_user_emulation.middleware import EmulationRemoteUserMiddleware


def dummy_get_response(self):
    client = Client()
    response = client.get('/')
    return response


class EmulationMiddlewareMockTests(SimpleTestCase):
    @patch('django_user_emulation.middleware.EmulationRemoteUserMiddleware')
    def test_init(self, my_middleware_mock):
        my_middleware = EmulationRemoteUserMiddleware('response')
        assert(my_middleware.get_response) == 'response'

    def test_mymiddleware(self):
        request = MagicMock()
        request.user = MagicMock()
        request.user.username = "testuser"
        request.user.is_authenticated = MagicMock(return_value=True)
        request.user.get_username = MagicMock(return_value="testuser")
        request.META = {
            "REMOTE_USER": "blah",
        }
        request.path = '/testURL/'
        request.session = {
            'is_emulating': True
        }
        my_middleware = EmulationRemoteUserMiddleware(Mock())
        # CALL MIDDLEWARE ON REQUEST HERE
        my_middleware(request)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertEqual(request.META["REMOTE_USER"], "testuser")
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.user.username, "testuser")
        self.assertTrue(request.session.get('is_emulating'))

    def test_mymiddleware_not_emulating(self):
        request = MagicMock()
        request.user = MagicMock()
        request.user.username = "testuser"
        request.user.is_authenticated = MagicMock(return_value=True)
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
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.user.username, "testuser")
        self.assertFalse(request.session.get('is_emulating', False))

    def test_mymiddleware_anonymous(self):
        request = Mock()
        request.user = AnonymousUser()
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
        self.assertEqual(request.user.username, "")

    def test_mymiddleware_noremote(self):
        request = Mock()
        request.user = AnonymousUser()
        request.user.username = "testuser"
        request.META = {}
        request.path = '/testURL/'
        request.session = {}
        my_middleware = EmulationRemoteUserMiddleware(Mock())
        # CALL MIDDLEWARE ON REQUEST HERE
        my_middleware(request)
        self.assertFalse("REMOTE_USER" in request.META)
        self.assertFalse(request.user.is_authenticated)
        self.assertEqual(request.user.username, "testuser")

    def test_mymiddleware_nouser(self):
        request = Mock()
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


class EmulationMiddlewareUnitTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username=self.superuser.username,
                          password='You shall not pass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = {}
        self.middleware = EmulationRemoteUserMiddleware(dummy_get_response)

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the gray')
        # create the logged in user which will the remote_user will become
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'You shall not pass')

    def test_requestProcessing(self):
        resp = self.middleware(self.request)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse("REMOTE_USER" in self.request.META)

    def test_requestProcessing_not_emulating(self):
        resp = self.middleware(self.request)
        request = resp.wsgi_request
        self.assertTrue("REMOTE_USER" not in request.META)
        self.assertFalse(request.user.is_authenticated)
        self.assertFalse(request.session.get('is_emulating', False))

    def test_requestProcessing_anonymous_user(self):
        # even if request.META is set, it will not exist on the response, will only do so if a logged in user is emulating
        request = self.request
        request.user = AnonymousUser()
        request.META["REMOTE_USER"] = self.user.username
        request.session['is_emulating'] = True
        self.middleware(request)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertFalse(request.user.is_authenticated)
        self.assertTrue(request.session.get('is_emulating', False))

    def test_requestProcessing_no_user(self):
        # remote_user is set but will not have results because there is no logged in user
        request = self.request
        request.META["REMOTE_USER"] = self.user.username
        request.session['is_emulating'] = True
        self.middleware(request)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertFalse("user" in request)
        self.assertTrue(request.session.get('is_emulating', False))

    def test_requestProcessing_emulated(self):
        request = self.request
        request.user = self.superuser
        request.META["REMOTE_USER"] = self.user.username
        request.session['is_emulating'] = True
        self.middleware(request)
        self.assertTrue(request.META["REMOTE_USER"])
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.META["REMOTE_USER"], self.superuser.username)

    def test_requestProcessing_emulate_self(self):
        request = self.request
        request.user = self.superuser
        request.META["REMOTE_USER"] = self.superuser.username
        request.session['is_emulating'] = True
        self.middleware(request)
        self.assertTrue("REMOTE_USER" in request.META)
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.META["REMOTE_USER"], self.superuser.username)

    def test_authenticate(self):
        self.assertIsNone(self.middleware.authenticate(self.request))


@override_settings(
    MIDDLEWARE=[
        "django_user_emulation.middleware.EmulationRemoteUserMiddleware"
    ]
)
class EmulationMiddlewareIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.login(username=self.superuser.username,
                          password='You shall not pass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/blah')
        self.request.session = {}
        self.middleware = EmulationRemoteUserMiddleware(dummy_get_response)

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the gray')
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'You shall not pass')

