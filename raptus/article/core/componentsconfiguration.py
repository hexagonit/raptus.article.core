
# -*- coding: utf-8 -*-
"""Utilities for looking up configuration for Components."""

from Products.CMFCore.utils import getToolByName
from raptus.article.core.interfaces import IArticle
from raptus.article.core.interfaces import IComponentsConfiguration
from zope.component import adapts
from zope.interface import implements


class ComponentsConfiguration(object):
    """Provides lookup of Components configuration."""
    implements(IComponentsConfiguration)
    adapts(IArticle)

    def __init__(self, context):
        self.context = context

    def get(self, key, default=None):
        """Find the requested key in portal_properties and return it's
        value.
        """
        props = getToolByName(self.context, 'portal_properties').raptus_article
        return props.getProperty(key, default)
