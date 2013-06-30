# Django Model URLs

This app has a purpose of making urls usage DRYer.
It allows to map a URL to a model object instance by passing the object instance
as argument to the URL.

## See in action

All examples will use these sample models:

```python
class Page(models.Model):
    slug = models.SlugField()
    category = models.ForeignKey('PageCategory')
    title = models.CharField(max_length=50)
```

And will attempt to generate this kind of URL pattern :

```
/page/2012/11/how-to-optimize-django-urls/
```

Therefore we'll have this in urls.py:

```python
urlpatterns = ('',
    url(r'^page/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$',
        'page.views.display',
        name='page_display'),
)
```

### Classical way django URL

#### In a views.py

```python
page = Page.objects.get(id=1)
return HttpResponseRedirect(reverse('page_display', args={
    'year': page.year,
    'month': page.month,
    'slug': page.slug,
}))
```

#### In a template

```jinja
{% url page_display page.year page.month, page.slug %}
```


### Now using django-model-urls

#### In a views.py

```python
page = Page.objects.get(id=1)
return HttpResponseRedirect(reverse('page_display', page))
```

#### In a template

```jinja
{% url page_display page %}
```

## Installation

### Download via pip

```
pip install -e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls
```

or add the line below to your pip requirements :

```
-e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls
```

### Update your settings

settings.py:

```python
INSTALLED_APPS = (
    'model_urls',
)
```

## Usage

### Defining model URLs

Model URL are generated _from a different pattern than the urlpatterns_.
Therefore you will need to define the `model_urls` in urls.py:

```python
model_urls = (
    (url_name, url_pattern, instance_attribute_names),
)
```

`model_urls` is a tuple of `model_url` tuple.

A model URL tuple has 3 parts:

1. a string: the name of the model URL
2. a string: a pattern containing attributes name. ie: "/page/%(year)d/%(month)s/%(slug)s/"
3. a tuple of strings: attributes to inject from instance into the pattern


> You may access to values of a foreignkey from the instance.
> To do so, use "__" (double underscores) in the pattern (just like for django ORM)
> and regular python "." for intance attribute names.
> ex: ('page_display', '/page/%(category__type)s/%(slug)s/', ('category.type', 'slug'))

#### In a template

```jinja
{% load modelurl %}
<a href="{% model_url 'page_display' page %}">view in details</a>
```

where `page_display` is the model URL key name and `page` is the instance passed
from the view.

#### In a view

```python
from model_url.urlresolver import reverse

page = Page.objects.get(id=1)
return HttpResponseRedirect(reverse('page_display', page))
```

In the future, I wish to drop the `model_urls` completely from urls.py, but so far
it must be used.

## Notice

`model_urls` in urls.py is a temporary way to generate a URL.
It is not as DRY as it could.
In the future, I hope to be able to generate it directly from the native urlpatterns.
If you have any suggestion about it, feel free to fork or let me know.


### Further examples

Refer to [tests.py](https://github.com/vinyll/django-model-urls/blob/master/model_urls/tests.py) to see more usages.
