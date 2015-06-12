from django.test import TestCase, Client
from main.models import User
from django.core.urlresolvers import reverse


class UserTestCase(TestCase):

    def Setup(self):
        self.client = Client()

    def test_ensure_registration_with_not_null_username_password(self):
        """
        Results True for Users registering with correct credintials,
        redirects to index.html

        Author: Aly Yakan
        """
        response = self.client.post(
                        reverse('register'),
                        {'username': u'markdoe',
                         'email': u'mark@gmail.com',
                         'password': u'123456'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.get(username='markdoe') is None)

    def test_ensure_registration_with_null_username_password(self):
        """
        Results False for Users registering with false credintials,
        redirects to index.html

        Author: Aly Yakan
        """
        response = self.client.post(
                        reverse('register'),
                        {'username': u'markdoe',
                         'email': u'mark@gmail.com',
                         'password': u''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

    def test_ensure_login_with_correct_credintials(self):
        """
        Results True for Users logging in with correct credintials, redirects
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
        Prevents Users logging in with wrong credintials, stays on
        same page

        Author: Aly Yakan
        """
        User.objects.create_user(username='johnnydoe',
                                 password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johndoe', 'password': '4567'})
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(user_logged_in)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # self.assertTrue(user_logged_out)

    def test_ensure_logout_when_logged_in(self):
        User.objects.create_user(username='johnnydoe',
                                 password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johndoe', 'password': '4567'})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('logout'))
        # self.assertEqual(response.status_code, 302)
