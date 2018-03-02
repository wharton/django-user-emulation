from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware


from django_user_emulation.context_processors import emulation


class EmulationViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.superuser = get_user_model().objects.create_superuser(
            'gandalf the white', 'gandalf@fellowship.org', 'fireworks')

    def test_emulation_off(self):
        request = self.factory.get('/blah')
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        result = emulation(request)
        self.assertFalse(result['is_emulating'])

    def test_emulation_on(self):
        request = self.factory.get('/blah')
        request.user = self.superuser
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session['is_emulating'] = True
        request.session.save()
        result = emulation(request)
        self.assertTrue(result['is_emulating'])
