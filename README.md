# Django Model URLs

This app has a purpose of making urls usage DRYer.
It allows to map a url to a model object instance by passing the object instance
as argument to the url.

### What's the problem ?

Let's say we have an Article with these attributes: year, month, slug, and few others

Let's say that we have in urls.py :

    urlpatterns = ('',
        …
        url(r'^cours/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$',
            'article.views.details',
            name='article_details'),
        )

We might call it multiple times in various templates :

    {% url article_details article.year article.month, article.slug %}


Someday, you need to add the "day" attribute to the Article and make it appear
in the url.
You also have to find each template where you were rendering this url.
Failing here would occur 404 errors or even 500.


### Solution: Model-urls to the rescue

Model-urls will help you rendering a url this way :

    {% url 'article_details' article %}


## Installation

### Download via pip

    pip install -e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls

or add the line below to your pip requirements :

    -e git+git://github.com/vinyll/django-model-urls.git#egg=django-model-urls


### Update your settings

settings.py :

    INSTALLED_APPS = (
        …,
        'model_urls',
        )


## How it works

1. Template calls "model_url" templatetag with view name and instance as arguments
2. Templatetags looks for the view name inside model_urls (in urls.py)
3. It translate the expression matching view name with the instance attributes.

A model_urls is a tuple of tuple located in urls.py and called "model_urls".
It has this structure :

    model_urls = (
        (view_name, url_pattern, instance_attributes),
        )

In the future, I wish to drop the model_urls completely from urls.py, but so far
it must be used.


## Usage examples

### Preset

In an existing project, you don't need these example presets, so you may skip
to "Configuring urls"

All example below will assume this model :

    class Page(models.Model):
        slug = models.SlugField()
        category = models.ForeignKey('PageCategory')
        title = models.CharField(max_length=50)

    class PageCategory(models.Model):
        name = models.CharField(max_length=50)
        slug = models.CharField(max_length=50)


And this sample data/fixture :

PageCategory > name: "Computer", slug: "computer"
Page > category: computer, title: "Django Cheatsheet", slug: "django-cheatsheet"

and rendering via this templatetag, assuming a Page instance called "page" :

    {% load url %}
    <a href="{% model_url 'page_show' page %}">read further</a>


### Configuring urls

#### Render a url like "/page/django-cheatsheet/"

urls.py:

    urlpatterns = ('',
        …
        url(r'^page/(?P<slug>[\w-]+)/$', 'page.views.show', name='page_show'),
        )
    model_urls = (
        ('page_show', (r'/page/%(slug)s/'), ('slug',))
        )


#### Render a url like "/page/django-cheatsheet/"

urls.py:

    urlpatterns = ('',
        …
        url(r'^page/(?P<slug>[\w-]+)/$', 'page.views.show', name='page_show'),
        )
    model_urls = (
        ('page_show', (r'/page/%(slug)s/'), ('slug',))
        )


#### Render a url like "/page/computer/django-cheatsheet/"

the model_urls is able to manage foreignkey attributes.
The idea is that the pattern must use double underscores "__" (like in django orm
foreignkey relation call) and instance parameters must use python style foreignkey
attribute call.

urls.py:

    urlpatterns = ('',
        …
        url(r'^page/(?P<category>[\w-]+)/(?P<slug>[\w-]+)/$', 'page.views.show', name='page_show'),
        )
    model_urls = (
        ('page_show', (r'/page/%(category__slug)s/%(slug)s/'), ('category.slug', 'slug'))
        )


### Further examples

Refer to tests.py to see more usages
