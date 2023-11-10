from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from register_app.models import Location, UserProfile, Project, SignInOutRegister
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.utils import timezone


class ViewTest(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        
        user_count_before = User.objects.count()
        post_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'test@trave.io',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'company_name': 'Test Company',
        }
        response = self.client.post(reverse('register'), post_data, follow=True)
        
        # Check if the form had errors
        if response.context and 'form' in response.context:
            form_errors = response.context['form'].errors
            if form_errors:
                print("Form errors:", form_errors.as_text())

        # Check if the user count has increased
        self.assertEqual(User.objects.count(), user_count_before + 1, "User count did not increase as expected")

        # Check the response redirect or content
        if response.status_code == 302:
            self.assertRedirects(response, reverse('user_dashboard'))
        else:
            print("Response content:", response.content.decode())


    def test_no_access_view(self):
        response = self.client.get(reverse('no_access'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_app/no_access.html')

    def test_admin_panel_view(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register_app/admin_panel.html')
        # Check for the presence of projects and clocked_in_users in context
        self.assertIn('projects', response.context)
        self.assertIn('clocked_in_users', response.context)
        



