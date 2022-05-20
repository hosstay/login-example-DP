from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from ..views import Register
from ..forms import RegisterForm

class RegisterTests(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.get(url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_register_url_resolves_register_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func.view_class, Register)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, RegisterForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulRegisterTests(TestCase):
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'johntesterman',
            'email': 'johntesterman@doe.com',
            'password1': 'Tester1!',
            'password2': 'Tester1!'
        }
        self.response = self.client.post(url, data)
        self.login_url = reverse('login')
        self.boards_url = reverse('boards')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the boards page
        '''
        self.assertRedirects(self.response, self.login_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

class InvalidRegisterTests(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_register_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())