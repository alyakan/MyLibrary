from django.test import TestCase, Client
from main.models import User
from django.core.urlresolvers import reverse


class UserTestCase(TestCase):

    def Setup(self):
        self.client = Client()

    def test_ensure_login_with_correct_credintials(self):
    	"""
        results True for Users logging in with correct credintials, redirects
        to index.html

        Author: Aly Yakan
        """
        User.objects.create_user(username='johndoe', password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johndoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)

    def test_deny_login_with_wrong_credintials(self):
    	"""
        prevents Users logging in with wrong credintials, stays on
        same page

        Author: Aly Yakan
        """
        User.objects.create_user(username='johnnydoe',
                                 password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johndoe', 'password': '4567'})
        self.assertEqual(response.status_code, 200)
