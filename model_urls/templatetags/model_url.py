from django.template import Library

from model_urls.urlresolvers import reverse

register = Library()

@register.simple_tag
def model_url(urlname, instance, urlconf=None):
    return reverse(urlname, instance, urlconf)