Introduction
============

This package provides a configurable article content type, which replaces the 
default Page content type.

The following features for raptus.article are provided by this package:

Content
-------
    * Article - Page Type - folderish

Components
----------
    * Related Items - Component - Component showing related Items.

Other
-----
    * zcml namespace (article) - used to initialize new components.

Installation
============

Standard range raptus.article
-----------------------------
**Important:**

- Note that it is recommended to use the raptus.article.default
  package which depends on the base components of raptus.article
  for more details have a look at the install documentation of 
  `raptus.article.default
  <http://pypi.python.org/pypi/raptus.article.default>`_.
  This installation only installs the core package.

- Note as well that it does not make sense to only install
  raptus.article.core if you don't develop your own add-ons or install other
  packages of raptus.article as it provides more or less the same functionality
  as the default Page content type.

Install raptus.article.core
---------------------------

To install raptus.article.core into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.core add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.core on a separate line, like this::

    eggs =
        Plone
        raptus.article.core

Next step is to add the zcml files to the "zcml" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other zcml's already
registered. Just add the raptus.article.core* on separate lines like this::

    eggs =
        Plone
        raptus.article.core-meta
        raptus.article.core
        raptus.article.core-overrides

Once you have added these lines to your configuration file, it's time to run
buildout, so the system can add and set up raptus.article.core for you. Go to the
command line and from the root of your Plone instance (same directory as
buildout.cfg is located in) run buildout like this::

    $ bin/buildout

If everything went according to plan you now have raptus.article.core installed
in your Zope instance.

Next, start up Zope using::

    $ bin/instance fg

Next go to the "Add-ons" control panel in Plone as an administrator and
install the "raptus.article.core" product. You should then be able to add
a new content type called Article.

Usage
=====

Add article
-----------
If you add a new article you will get the standard plone form to add content.

Components
----------
By navigating to the "Components" tab you may select the components you would like
to have displayed by this article.

Note if you only installed the raptus.article.core package there is just
the component "Related Items" available. To add other components like image,
files or links visit the 
`pypi-site <http://pypi.python.org/pypi?%3Aaction=search&term=raptus.article&submit=search>`_
or install the package 
`raptus.article.default <http://pypi.python.org/pypi/raptus.article.default>`_. 

Additional components
=====================
If you install the default package like the core package, you will get automatically the usual types
like link, image, etc.. Besides if you install the article with default, you will not have to register
all packages in buildout.cfg. The default package find automatically all component packages of raptus.article.
For details read the doc of `default package <http://pypi.python.org/pypi/raptus.article.default/>`_.

- `raptus.article.default <http://pypi.python.org/pypi/raptus.article.default>`_
  (Installs all raptus article components present in your buildout.cfg).

If you decide to group your components by yourself, here is a list of all currently available components. 
Install the selected packages like ratpus.article.core. Just be careful not all packages have an overrides.zcml
and meta.zcml:

- `raptus.article.additionalwysiwyg <http://pypi.python.org/pypi/raptus.article.additionalwysiwyg/>`_
  (Provides an additional WYSIWYG text field for the articles)
  
- `raptus.article.contentfader <http://pypi.python.org/pypi/raptus.article.contentfader>`_
  (Provides a component which continually fades in and out the contained articles)
  
- `raptus.article.contentflow <http://pypi.python.org/pypi/raptus.article.contentflow>`_
  (Provides a content flow component like the one used in iTunes)
  
- `raptus.article.fader <http://pypi.python.org/pypi/raptus.article.fader>`_
  (Provides a component which continually fades in and out the contained images)
  
- `raptus.article.files <http://pypi.python.org/pypi/raptus.article.files>`_
  (Provides support for adding attachments to articles)
  
- `raptus.article.flash <http://pypi.python.org/pypi/raptus.article.flash>`_
  (Provides support for flash movies)
  
- `raptus.article.form <http://pypi.python.org/pypi/raptus.article.form>`_
  (Provides support for PloneFormGen)
  
- `raptus.article.gallery <http://pypi.python.org/pypi/raptus.article.gallery>`_
  (Provides basic gallery components)
  
- `raptus.article.header <http://pypi.python.org/pypi/raptus.article.header>`_
  (Provides header image support by integrating raptus.header in article)
  
- `raptus.article.hidecolumns <http://pypi.python.org/pypi/raptus.article.hidecolumns>`_
  (Provides functionality to hide the left or right portlet column per article)
  
- `raptus.article.images <http://pypi.python.org/pypi/raptus.article.images>`_
  (Provides support for adding images to articles)
  
- `raptus.article.lightbox <http://pypi.python.org/pypi/raptus.article.lightbox>`_
  (Provides an inline lightbox component showing the images contained in the article)
  
- `raptus.article.lightboxgallery <http://pypi.python.org/pypi/raptus.article.lightboxgallery>`_
  (Provides an inline lightbox component with a horizontal gallery showing the images contained in the article)
  
- `raptus.article.links <http://pypi.python.org/pypi/raptus.article.links>`_
  (Provides support for adding links to articles)
  
- `raptus.article.listings <http://pypi.python.org/pypi/raptus.article.listings>`_
  (Provides basic listing components which display articles contained in the article)
  
- `raptus.article.maps <http://pypi.python.org/pypi/raptus.article.maps>`_
  (Provides a maps content type to be added to articles)
  
- `raptus.article.media <http://pypi.python.org/pypi/raptus.article.media>`_
  (Provides audio and video support for articles)
  
- `raptus.article.multilanguagefields <http://pypi.python.org/pypi/raptus.article.multilanguagefields>`_
  (Provides support for raptus.multilanguagefields in article)
  
- `raptus.article.nesting <http://pypi.python.org/pypi/raptus.article.nesting>`_
  (Provides nesting support for articles)
  
- `raptus.article.randomcontent <http://pypi.python.org/pypi/raptus.article.randomcontent>`_
  (Provides a component which displays a random article)
  
- `raptus.article.randomimage <http://pypi.python.org/pypi/raptus.article.randomimage>`_
  (Provides components which display a random image contained in the article)
  
- `raptus.article.reference <http://pypi.python.org/pypi/raptus.article.reference>`_
  (Provides support for internal or external references on nested articles)
  
- `raptus.article.table <http://pypi.python.org/pypi/raptus.article.table>`_
  (Provides a table component for articles)
  
- `raptus.article.teaser <http://pypi.python.org/pypi/raptus.article.teaser>`_
  (Provides support for a teaser image)
  
- `raptus.article.upload <http://pypi.python.org/pypi/raptus.article.upload>`_
  (Provides multiupload functionality for articles using collective.uploadify)

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
