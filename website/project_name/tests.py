from {{ project_name }}.test_helpers import ExtendedTestCase
from {{ project_name }} import models

class {{ project_name }}Tests(ExtendedTestCase):
    def signup_user(self):
        users = models.User.objects.count()
        self.post("/signup/", {"email": "user{}@example.com".format(users), "password": "foobar"})
        return models.User.objects.get(id=users+1)

    def test_404(self):
        self.assertStatus(404, '/foobar/')

    def test_home(self):
        self.assertStatus(200, '/')

    def test_login(self):
        self.assertStatus(200, '/login/')

    def test_logout(self):
        response = self.get('/logout/')
        self.assertRedirects(response, '/')

    def test_signup(self):
        self.assertStatus(200, '/signup/')
        user = self.signup_user()
        self.assertEqual(1, user.id)

