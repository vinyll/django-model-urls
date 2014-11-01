# Django Model URLs

[![Build Status](https://travis-ci.org/vinyll/django-model-urls.svg)](https://travis-ci.org/vinyll/django-model-urls)

This app makes urls usage DRYer.
It maps URL keywords to a model object instance by passing the object
instance as argument to the URL.

In short, having an `article` model instance, you can write this:

```html
<a href="{{ url('article:detail', article) }}">View this article</a>
```

While you have been writing this so far:

```html
<a href="{{ url('article:detail', year=article.year, month=article.month, slug=article.slug) }}">View this article</a>
```

This is for your templates as well as for your `reverse()` and preserves
other urls to work.

> Right now it is build for [Jinja2](http://jinja.pocoo.org/) using the
easy-to-use [Jingo](https://github.com/jbalogh/jingo) adapter.
> If you are using plain Django template, refer to version 0.3.1.
> A new version for plain Django should come out later on.


## Installation

Download via pip [![pip badge](https://pypip.in/version/django-model-urls/badge.svg)](https://pypi.python.org/pypi/django-model-urls/)

```bash
pip install django-model-urls
```

or get the bleeding edge version:

```bash
pip install git+https://github.com/vinyll/django-model-urls.git
```

Add _model\_urls_ to your _settings_ file:

```python
INSTALLED_APPS = (
    'jingo',
    'model_urls',
)
```

And you're done!


## How to use it

In the examples below we will consider this model:

```python
class Article(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=50)
    date = models.DateField()

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month
```

and this urls:

```python
urlpatterns = patterns('',
    url(r'^article/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[\w-]+)/$',
        ArticleView.as_view(), name="article_details"),
)
```

and `article` being an instance of the `Article` class.

### In a template

```python
url('article_details', article)
```

#### In a view

```python
from model_urls.urlresolvers import reverse

reverse('article_details', article)
```

Both will generate a url in this format:

```
/2014/11/how-to-optimize-django-urls/
```

## Extra tools

Basically you should be able to use `url()` and `reverse()` in all cases.
However, these tools are also available:


#### Template helpers

- `url(viewname, *args, **kwargs)` will try to detect an instance in arguments
and choose wheter to use _simple\_url()_ or _model\_url()_ otherwise.
- `simple_url(viewname, *args, **kwargs)` is an alias to Jingo's `url()`
helper to force using it.
- `model_url(viewname, instance, *args, **kwargs)` will generate the url from
the instance in first argument.


#### Url reversing

These functions are available in `model_urls.urlresolvers`.

- `model_reverse(viewname, instance, urlconf=None, args=None, kwargs=None,
prefix=None, current_app=None)` will generate the url based on the instance
properties.
- `reverse(viewname, *args, **kwargs)` will fallback to _model\_reverse()_ if
an instance is found in arguments or to Django's _reverse()_ otherwise.


## Configuration

An optional configuration is for your settings is:

```python
MODEL_URLS_HELPER_OVERRIDE = False
```

This option will not allow the Jingo's `url()` helper to be overriden by the
one from model_urls.

In this case you should use `model_url()` to use an instance.



### Further examples

#### Use cases

A common use case is switching from pk based url to slug.
Using django-model-urls means updating the _urls.py_ file to consider slug
without altering views or template files.


#### Read tests

Refer to [tests.py](https://github.com/vinyll/django-model-urls/blob/master/model_urls/tests/)
to see more usages.
