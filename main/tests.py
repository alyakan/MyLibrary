from django.test import TestCase, Client
from main.models import User, Library, Book
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


class LibraryTestCase(TestCase):

    def Setup(self):
        self.client = Client()

    def test_ensure_library_created_with_not_null_name(self):
        """
        Ensures a library is created with correct information

        Author: Aly Yakan
        """
        User.objects.create_user(username='johnnydoe',
                                 password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johnnydoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='johnnydoe')
        response = self.client.post(
            reverse('library-add'),
            {'name': 'johnnylibrary',
             'location': 'here',
             'owner': user.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Library.objects.all().count(), 1)
        self.assertFalse((Library.objects.get(name='johnnylibrary') is None))

    def test_ensure_library_not_created_with_null_name(self):
        """
        Ensures a library is not created with null name

        Author: Aly Yakan
        """
        User.objects.create_user(username='johnnydoe',
                                 password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johnnydoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='johnnydoe')
        response = self.client.post(
            reverse('library-add'),
            {'name': '',
             'location': 'here',
             'owner': user.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Library.objects.all().count(), 0)

    def test_list_view_not_signed_in(self):
        """
        Ensures a guest can browse libraries from
        libraries' list view

        Author: Aly Yakan
        """
        user1 = User.objects.create_user(username='johndoe',
                                         password='123456')
        user2 = User.objects.create_user(username='johnnydoe',
                                         password='123456')
        response = self.client.post(
            reverse('library-add'),
            {'name': u'Cairo Library',
             'location': u'Cairo',
             'owner': user1.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse('library-add'),
            {'name': u'Texas Library',
             'location': u'Texas',
             'owner': user2.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/main/library-list/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        self.assertEqual(
            [Library.pk for Library in response.context['object_list']],
            [1, 2])

    def test_library_detailed_view_not_signed_in(self):
        """
        Ensures a guest can access a library's detailed view

        Author: Aly Yakan
        """
        user = User.objects.create_user(username='johndoe',
                                        password='123456')
        response = self.client.post(
            reverse('library-add'),
            {'name': u'Cairo Library',
             'location': u'Cairo',
             'owner': user.id})
        self.assertEqual(response.status_code, 302)
        lib_slug = Library.objects.get(owner=user.id).slug
        response = self.client.get('/main/mylibrary/' + lib_slug + '/')
        self.assertEqual(response.status_code, 200)


class BookTestCase(TestCase):

    def Setup(self):
        self.client = Client()

    def test_ensure_book_created_with_not_null_name(self):
        """
        Ensures a book is created with correct information

        Author: Aly Yakan
        """
        user = User.objects.create_user(username='johnnydoe',
                                        password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johnnydoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        lib = Library.objects.create(name='johnnylibrary',
                                     location='here',
                                     owner=user)
        response = self.client.post(
            reverse('book-add', kwargs={'slug': lib.slug}),
            {'name': u'johnnydoe',
             'author': 'johnny',
             'library': lib.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Book.objects.all().count(), 1)

    def test_ensure_book_not_created_with_null_name(self):
        """
        Ensures a book is not created with wrong information

        Author: Aly Yakan
        """
        user = User.objects.create_user(username='johnnydoe',
                                        password='123456')
        response = self.client.post(
            reverse('login'),
            {'username': u'johnnydoe', 'password': '123456'})
        self.assertEqual(response.status_code, 302)
        lib = Library.objects.create(name='johnnylibrary',
                                     location='here',
                                     owner=user)
        response = self.client.post(
            reverse('book-add', kwargs={'slug': lib.slug}),
            {'name': '',
             'author': 'johnny',
             'library': lib.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.all().count(), 0)

    def test_book_detailed_view_not_signed_in(self):
        """
        Ensures a guest can access a book's detailed view

        Author: Aly Yakan
        """
        user = User.objects.create_user(username='johndoe',
                                        password='123456')
        lib = Library.objects.create(name='library',
                                     location='here',
                                     owner=user)
        book = Book.objects.create(name='mybook',
                                   author='me',
                                   library=lib)
        response = self.client.get('/main/mylibrary/' +
                                   lib.slug +
                                   '/book/' +
                                   book.slug +
                                   '/')
        self.assertEqual(response.status_code, 200)

    def test_book_list_view_not_signed_in(self):
        """
        Ensures a guest can access books list view

        Author: Aly Yakan
        """
        user = User.objects.create_user(username='johndoe',
                                        password='123456')
        lib = Library.objects.create(name='library',
                                     location='here',
                                     owner=user)
        response = self.client.post(
            reverse('book-add', kwargs={'slug': lib.slug}),
            {'name': u'My Book',
             'author': u'Me',
             'library': lib.id})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            reverse('book-add', kwargs={'slug': lib.slug}),
            {'name': u'My Book 2',
             'author': u'Me',
             'library': lib.id})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/main/book-list/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        self.assertEqual(
            [Book.pk for Book in response.context['object_list']],
            [1, 2])
