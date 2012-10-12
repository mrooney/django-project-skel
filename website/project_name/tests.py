from {{ project_name }}.test_helpers import ExtendedTestCase
from {{ project_name }} import models

class {{ project_name }}Tests(ExtendedTestCase):
    def setUp(self):
        self.post("/signup/", {"email": "test@example.com", "password": "foobar"})
        self.user = models.User.objects.get(id=1)

    def test_404(self):
        self.assertStatus(404, '/foobar/')

    def test_home(self):
        self.assertStatus(200, '/')

