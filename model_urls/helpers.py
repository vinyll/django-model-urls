from django.conf import settings

from jingo import register

from .urlresolvers import model_reverse, dj_reverse, reverse


@register.function(override=getattr(settings, 'MODEL_URLS_HELPER_OVERRIDE',
                                    True))
def url(viewname, *args, **kwargs):
    """
    Override the default Jingo helper to use model_urls ``reverse()``.
    """
    urlconf = kwargs.pop('urlconf') if 'urlconf' in kwargs else None
    return reverse(viewname, args=args, kwargs=kwargs,
                   urlconf=urlconf)


@register.function
def model_url(viewname, instance, *args, **kwargs):
    """
    Template helper to use model_urls ``reverse()``.
    """
    urlconf = kwargs.pop('urlconf') if 'urlconf' in kwargs else None
    return model_reverse(viewname, instance=instance, args=args, kwargs=kwargs,
                         urlconf=urlconf)


@register.function
def simple_url(viewname, *args, **kwargs):
    """
    Native ``reverse()`` call, Jingo's style.
    """
    urlconf = kwargs.pop('urlconf') if 'urlconf' in kwargs else None
    return dj_reverse(viewname, args=args, kwargs=kwargs, urlconf=urlconf)
