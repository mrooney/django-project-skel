from {{ project_name }}.test_helpers import ExtendedTestCase

class {{ project_name }}Tests(ExtendedTestCase):
    def test_404(self):
        self.assertStatus(404, '/foobar/')

    def test_home(self):
        self.assertStatus(200, '/')

