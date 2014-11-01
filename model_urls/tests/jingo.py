from django.test import TestCase

from model_urls.helpers import simple_url, model_url, url
from model_urls.urlresolvers import reverse, dj_reverse, model_reverse

from model_urls.tests.models import DummyModel


urlconf = 'model_urls.tests.urls'


dummy = DummyModel("my-name",
                   ref=DummyModel("my-ref",
                                  ref=DummyModel("its-ref")))


class ReverseTest(TestCase):

    def test_original_reverse(self):
        self.assertEqual(dj_reverse('basic_path', urlconf=urlconf), "/path/")

    def test_model_reverse(self):
        self.assertEqual(model_reverse('url_name', dummy, urlconf=urlconf),
                         "/path/my-name/")

    def test_overridden_reverse(self):
        self.assertEqual(reverse('basic_path', urlconf), "/path/")
        self.assertEqual(reverse('url_name', dummy, urlconf),
                         "/path/my-name/")

    def test_reverse_multiple_kwargs(self):
        self.assertEqual(reverse('url_mixed', dummy, urlconf),
                         "/path/my-name/my-ref/8/")

    def test_reverse_namespaced(self):
        self.assertEqual(reverse('app:pk_path', dummy, urlconf),
                         "/app/about/8/")


class UrlHelperTest(TestCase):

    def test_simple_url(self):
        self.assertEqual(simple_url('basic_path', urlconf=urlconf), "/path/")
        self.assertEqual(simple_url('url_name', 'john', urlconf=urlconf),
                         "/path/john/")

    def test_model_url(self):
        self.assertEqual(model_url('url_name', dummy, urlconf=urlconf),
                         "/path/my-name/")

    def test_overridden_url(self):
        self.assertEqual(url('url_name', dummy, urlconf=urlconf),
                         "/path/my-name/")
