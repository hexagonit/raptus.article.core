# -*- coding: utf-8 -*-
"""A dummy component that we can use in our tests."""

from plone.app.layout.viewlets.common import ViewletBase

from zope import component
from zope import interface

from raptus.article.core.interfaces import IArticle
from raptus.article.core.interfaces import IComponent
from raptus.article.core.interfaces import IComponentSelection


class IFoo(interface.Interface):
    """Marker interface for the Foo viewlet."""


class Foo(object):
    """Component which displays Foo."""
    interface.implements(IComponent, IComponentSelection)
    component.adapts(IArticle)

    title = u'Foo'
    image = '++resource++foo.gif'
    interface = IFoo
    viewlet = 'raptus.article.foo'

    def __init__(self, context):
        self.context = context


class ViewletFoo(ViewletBase):
    """Viewlet for Foo."""
    pass
