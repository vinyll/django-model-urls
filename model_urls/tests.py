from django.test import TestCase

from model_urls.urlresolvers import reverse
from model_urls.templatetags.modelurl import model_url


model_urls = (
    ('url1', (r'/cours/')),
    ('url2', (r'/cours/%(name)s/', ('name',))),
    ('url3', (r'/cours/%(name)s/%(ref__ref__name)s/', ('name', 'ref.ref.name'))),
    )

class DummyModel(object):
    def __init__(self, name="dummy-model", ref=None):
        self.name = name
        self.ref = ref

urlconf = 'model_urls.tests'

class UrlsReverseTest(TestCase):
    def setUp(self):
        self.instance = DummyModel(ref=DummyModel(ref=DummyModel('endpoint')))

    def test_reverse_empty(self):
        self.assertEqual(reverse('url1', self.instance, urlconf), r'/cours/')

    def test_reverse_attr(self):
        self.assertEqual(reverse('url2', self.instance, urlconf), r'/cours/dummy-model/')

    def test_reverse_deep_attr(self):
        self.assertEqual(reverse('url3', self.instance, urlconf), r'/cours/dummy-model/endpoint/')

    def test_templatetag_model_url_deep_attr(self):
        self.assertEqual(model_url('url3', self.instance, urlconf), r'/cours/dummy-model/endpoint/')