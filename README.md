# Django Model URLs

This app has a purpose of making urls usage DRYer.
It allows to map a url to a model object instance by passing the object instance
as argument to the url.

## See in action

All examples will use these sample models:

    class Page(models.Model):
        slug = models.SlugField()
        category = models.ForeignKey('PageCategory')
        title = models.CharField(max_length=50)

And will attempt to generate this kind of url pattern :

    /page/2012/11/how-to-optimize-django-urls/

Therefore we'll have this in urls.py:

    urlpatterns = ('',
        …
        url(r'^page/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$',
            'page.views.display',
            name='page_display'),
        )


#### Classical way django url

##### in a views.py

    …
    page = Page.objects.get(id=1)
    return HttpResponseRedirect(reverse('page_display', args={
            'year': page.year,
            'month': page.month,
            'slug': page.slug,
        }))

###### in a template

    {% url page_display page.year page.month, page.slug %}


#### Now using django-model-urls

##### in a views.py

    …
    page = Page.objects.get(id=1)
    return HttpResponseRedirect(reverse('page_display', page))

###### in a template

    {% url page_display page %}


## Installation

### Download via pip

    pip install -e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls

or add the line below to your pip requirements :

    -e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls


### Update your settings

settings.py:

    INSTALLED_APPS = (
        …,
        'model_urls',
        )


## Usage

#### Defining model urls

Model url are generated **from a different pattern than the urlpatterns**.
Therefore you will need to **define the _model\_urls_** in urls.py:

    …
    model_urls = (
        (url_name, url_pattern, instance_attribute_names),
        )

_model_urls_ is a tuple of model_url tuple.
A model url tuple has 3 parts:

1. a string: the name of the model url
2. a string: a pattern containing attributes name. ie: "/page/%(year)d/%(month)s/%(slug)s/"
3. a tuple of strings: attributes to inject from instance into the pattern

> you may access to values of a foreignkey from the instance.
> To do so, use "__" (double underscores) in the pattern (just like for django orm)
> and regular python "." for intance attribute names.
> ex: ('page_display', '/page/%(category__type)s/%(slug)s/', ('category.type', 'slug'))

#### In a template

    {% load modelurl %}
    <a href="{% model_url 'page_display' page %}">view in details</a>

where _page_display_ is the model url key name and _page_ is the instance passed
from the view.

#### In a view

    from model_url.urlresolver import reverse
    …
    page = Page.objects.get(id=1)
    return HttpResponseRedirect(reverse('page_display', page))


In the future, I wish to drop the model_urls completely from urls.py, but so far
it must be used.

## Notice

model_urls in urls.py is a temporary way to generate a url.
It is not as DRY as it could.
In the future, I hope to be able to generate it directly from the native urlpatterns.
If you have any suggestion about it, feel free to fork or let me know.


### Further examples

Refer to [tests.py](https://github.com/vinyll/django-model-urls/blob/master/model_urls/tests.py) to see more usages
