from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class AliceBobTestCase(TestCase):
    fixtures = ['alice_bob.json']
    password = 'P@55w0rd'
    ALICE_PUBLIC_TITLE = 'alice public post'
    ALICE_PRIVATE_TITLE = 'alice private post'

    def auth_bob(self):
        self.client.login(username='Bob', password=self.password)

    def auth_alice(self):
        self.client.login(username='Alice', password=self.password)

    def get_post(self, author, title):
        return self.client.get(reverse(
            'blog_platform.views.display_post', kwargs={
                'author': author,
                'slug': slugify(title),
            }
        ))

    def get_alice_public_post(self):
        return self.get_post('Alice', self.ALICE_PUBLIC_TITLE)

    def get_alice_private_post(self):
        return self.get_post('Alice', self.ALICE_PRIVATE_TITLE)

    def test_bob_sees_public_in_list(self):
        self.auth_bob()
        response = self.client.get(reverse('blog_platform.views.display_latest_posts'))
        self.assertIn(self.ALICE_PUBLIC_TITLE, response.content)
        self.assertNotIn(self.ALICE_PRIVATE_TITLE, response.content)

    def test_alice_sees_private_in_list(self):
        self.auth_alice()
        response = self.client.get(reverse('blog_platform.views.display_latest_posts'))
        self.assertIn(self.ALICE_PUBLIC_TITLE, response.content)
        self.assertIn(self.ALICE_PRIVATE_TITLE, response.content)

    def test_bob_doesnt_sees_private_details(self):
        self.auth_bob()
        response = self.get_alice_private_post()
        self.assertEqual(response.status_code, 404)

    def test_bob_sees_public_details(self):
        self.auth_bob()
        response = self.get_alice_public_post()
        self.assertIn(self.ALICE_PUBLIC_TITLE, response.content)

    def test_alice_sees_private_details(self):
        self.auth_alice()
        response = self.get_alice_private_post()
        self.assertIn(self.ALICE_PRIVATE_TITLE, response.content)

    def test_alice_sees_public_details(self):
        self.auth_alice()
        response = self.get_alice_public_post()
        self.assertIn(self.ALICE_PUBLIC_TITLE, response.content)
