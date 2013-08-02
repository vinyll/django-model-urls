from django.core.urlresolvers import reverse as dj_reverse, get_urlconf, get_resolver


def obj_hasattr(obj, attr):
    if hasattr(obj, attr):
        return True
    if "__" in attr:
        parts = attr.split("__")
        return hasattr(getattr(obj, parts[0]), parts[1])


def obj_getattr(obj, attr, default=None):
    if getattr(obj, attr, None):
        return getattr(obj, attr)
    if "__" in attr:
        parts = attr.split("__")
        parts.reverse()
        while parts:
            obj = getattr(obj, parts.pop())
    return obj


def obj_hasattrs(obj, attrs):
    for attr in attrs:
        if not obj_hasattr(obj, attr):
            return False
    return True


def reverse(viewname, instance=None, urlconf=None, **kwargs):
    kwargs['urlconf'] = urlconf
    attrs = {}
    for pattern in get_resolver(get_urlconf(urlconf)).url_patterns:
        kws = pattern.regex.groupindex.keys()
        if pattern.name == viewname and obj_hasattrs(instance, kws):
            attrs = dict([(k, obj_getattr(instance, k)) for k in kws])
    return dj_reverse(viewname, kwargs=attrs, **kwargs)
