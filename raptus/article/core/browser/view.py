# -*- coding: utf-8 -*-
"""Main Article view."""

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from raptus.article.core import interfaces
from zope.interface import implements


class View(BrowserView):
    """View of an article."""
    implements(interfaces.IArticleView)
    template = ViewPageTemplateFile('view.pt')

    def __call__(self):
        return self.template()
