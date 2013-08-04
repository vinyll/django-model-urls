from django.test import TestCase
from django.http import HttpResponse
from django.conf.urls import patterns, include, url

from model_urls.urlresolvers import reverse, obj_getattr
from model_urls.templatetags.model_url import model_url


class DummyModel(object):

    def __init__(self, name="dummy-model", ref=None):
        self.name = name
        self.ref = ref

dummy_model = DummyModel(ref=DummyModel(name="level2",
                                        ref=DummyModel('endpoint')))


urlpatterns = patterns('',
   url(r'^path/$', lambda r: HttpResponse(""), name="basic_path"),
   url(r'^path/(?P<name>.+)/$', lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", mimetype="text/plain"),
       name='instance_path'),
   url(r'^path/(?P<ref__name>.+)/$', lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", mimetype="text/plain"),
       name='ref_instance_path'),
   url(r'^path/(?P<ref__ref__name>.+)/$', lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", mimetype="text/plain"),
       name='ref_deep_path'),
   url(r'^path/(?P<name>.+)/(?P<ref__name>.+)/(?P<ref__ref__name>.+)/$',
       lambda r: HttpResponse(
            "User-agent: *\nDisallow: /", mimetype="text/plain"),
       name='ref_instance_multiple_path'),
   )

urlconf = 'model_urls.tests'


class ObjAttrTest(TestCase):

    def test_simple_obj_getattr(self):
        self.assertEqual(obj_getattr(dummy_model, 'name'), "dummy-model")

    def test_level_obj_getattr(self):
        self.assertEqual(obj_getattr(dummy_model, 'ref__name'), "level2")

    def test_deep_obj_getattr(self):
        self.assertEqual(
            obj_getattr(dummy_model, 'ref__ref__name'), "endpoint")


class UrlsReverseTest(TestCase):

    def setUp(self):
        dummy_model = DummyModel(
            ref=DummyModel(name="level2", ref=DummyModel('endpoint')))

    def test_default_reverse(self):
        self.assertEqual(reverse('basic_path', urlconf=urlconf), "/path/")

    def test_instance_reverse(self):
        self.assertEqual(
            reverse('instance_path', dummy_model, urlconf=urlconf),
            "/path/dummy-model/")

    def test_level_reverse(self):
        self.assertEqual(
            reverse('ref_instance_path', dummy_model, urlconf),
            r'/path/level2/')

    def test_deep_reverse(self):
        self.assertEqual(
            reverse('ref_deep_path', dummy_model, urlconf), r'/path/endpoint/')

    def test_multiple_attributes_reverse(self):
        self.assertEqual(
            reverse('ref_instance_multiple_path', dummy_model, urlconf),
            r'/path/dummy-model/level2/endpoint/')
