from django.conf import settings
from django.core.urlresolvers import (get_urlconf, NoReverseMatch,
                                      get_resolver, reverse as dj_reverse)


def model_reverse(viewname, instance, urlconf=None, args=None, kwargs=None,
                  prefix=None, current_app=None):
    """
    Calculates an url from a view name when passing a dictable object
    (such a Model instance) as parameter.
    The function will parse the url pattern and attempt to match the instance
    properties with the urlpattern kwargs.
    """
    matching_pattern = None
    if urlconf is None:
        urlconf = get_urlconf()
    resolver = get_resolver(urlconf)
    possibilities = []
    (namespace, url) = (None, viewname)
    if ":" in viewname:
        (namespace, url) = viewname.split(":")
    for urlpattern in resolver.url_patterns:
        possibilities.append(urlpattern)
        if ((not hasattr(urlpattern, 'namespace') and not namespace)
            or (hasattr(urlpattern, 'namespace')
                and urlpattern.namespace == namespace)):
            if hasattr(urlpattern, 'url_patterns'):
                for subpattern in urlpattern.url_patterns:
                    if subpattern.name == url:
                        matching_pattern = subpattern
            else:
                if urlpattern.name == url:
                    matching_pattern = urlpattern
    try:
        kwarg_keys = matching_pattern.regex.groupindex.keys()
    except AttributeError:
        raise NoReverseMatch("Reverse for '%s' with instance '%s' of class "
                             "'%s' not found. %d pattern(s) tried: %s" %
                             (viewname, instance, instance.__class__,
                              len(possibilities), possibilities))
    kwargs = {}
    for key in kwarg_keys:
        kwargs[key] = str(getattr(instance, key, None))
    return dj_reverse(viewname, urlconf=urlconf, prefix=prefix,
                      current_app=current_app, args=args, kwargs=kwargs)


def reverse(viewname, *args, **kwargs):
    """
    Resolved a viewname accepting a model `instance` argument or a first
    argument being a model `instance`. Any `dict` object could actually be
    passed.
    The viewname will then match properties from the dict to the view kwargs.
    """
    instance = None
    # instance is a kwargs
    if 'instance' in kwargs:
        instance = kwargs.pop('instance')
    # instance is the first arg
    elif len(args) and hasattr(args[0], '__dict__'):
        instance = args[0]
        args = args[1:]
    # instance is the first arg in url()
    elif('args' in kwargs and len(kwargs['args'])
         and hasattr(kwargs['args'][0], '__dict__')):
        instance = kwargs.pop('args')[0]

    if instance:
        return model_reverse(viewname, instance, *args, **kwargs)

    return dj_reverse(viewname, *args, **kwargs)
