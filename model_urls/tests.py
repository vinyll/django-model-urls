from django.test import TestCase
from model_urls.templatetags.url import model_url


model_urls = (
    ('url1', (r'/cours/')),
    ('url2', (r'/cours/%(name)s/', ('name',))),
    ('url3', (r'/cours/%(name)s/%(ref__ref__name)s/', ('name', 'ref.ref.name'))),
    )

class DummyModel(object):
    def __init__(self, name="dummy-model", ref=None):
        self.name = name
        self.ref = ref

class UrlsTemplatetagTest(TestCase):
    def setUp(self):
        self.instance = DummyModel(ref=DummyModel(ref=DummyModel('endpoint')))
    def test_model_url_empty(self):
        self.assertEqual(model_url('url1', self.instance, 'model_urls.tests'), r'/cours/')
    def test_model_url_attr(self):
        self.assertEqual(model_url('url2', self.instance, 'model_urls.tests'), r'/cours/dummy-model/')
    def test_model_url_deep_attr(self):
        self.assertEqual(model_url('url3', self.instance, 'model_urls.tests'), r'/cours/dummy-model/endpoint/')