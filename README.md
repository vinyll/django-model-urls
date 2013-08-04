# Django Model URLs

This app has a purpose of making urls usage DRYer.
It allows to map a URL to a model object instance by passing the object instance
as argument to the URL.

[![Build Status](https://travis-ci.org/vinyll/django-model-urls.png)](https://travis-ci.org/vinyll/django-model-urls)

## Installation

Download via pip

```bash
pip install -e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls
```

or add the line below to your pip requirements :

```bash
-e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls
```

Add _model_urls_ to your _settings_ file:

```python
INSTALLED_APPS = (
    'model_urls',
)
```


## How to use it


### Example

Assuming you have this url:

```python
urlpatterns = patterns('',
    url(r'^page/(?<category__slug>.+)/(?<slug>.+)/$',
        PageDetailView.as_view(),
        name="page_detail"),
    …
)
```

this model:

```python
class Page(models.Model):
    slug = models.SlugField()
    category = models.ForeignKey('PageCategory')
    title = models.CharField(max_length=50)

class PageCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
```

This instance object:

```python
django = PageCategory(slug="django-tips", name="Django tips and tricks")
Page.objects.create(category=django, slug="easy-urls-with-django")
```

Then, a call to `{% model_url "page_detail" page %}` would generate a url like
`/page/django-tips/how-to-optimize-django-urls/`


#### In a template

```html
{% load model_url %}
<a href="{% model_url 'page_detail' page %}">view in details</a>
```

where `page` is the model instance.


#### In a view

```python
from model_url.urlresolver import reverse

page = Page.objects.get(id=1)
return HttpResponseRedirect(reverse('page_detail', page))
```

### Further examples

#### Use cases

A common use case is switching from pk based url to slug.
Using django-model-urls means updating the _urls.py_ file to consider slug
without altering views or template files.


#### See tests

Refer to [tests.py](https://github.com/vinyll/django-model-urls/blob/master/model_urls/tests.py)
to see more usages.
