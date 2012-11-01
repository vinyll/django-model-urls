from django.template import Library
from django.core.urlresolvers import get_urlconf, get_resolver


register = Library()

@register.simple_tag
def model_url(url_name, instance, urlconf=None):
    model_urls = getattr(get_resolver(get_urlconf(urlconf)).urlconf_module, 'model_urls')
    url_dict = dict(model_urls)[url_name]
    key_val = {}
    if not isinstance(url_dict, (tuple, list)):
        return url_dict
    for key in url_dict[1]:
        try:
            key_val[key.replace('.', '__')] = reduce(getattr, key.split('.'), instance)
        except AttributeError, e:
            raise AttributeError(
                'Error parsing model_url "%s" with instance "%s" : %s' %\
                (url_name, instance, e.message))
    try:
        uri = url_dict[0] % key_val
    except TypeError, e:
        raise AttributeError(
            'Error substituting values for model_url "%s" with instance "%s" : %s' %\
            (url_name, instance, e.message))
    return uri