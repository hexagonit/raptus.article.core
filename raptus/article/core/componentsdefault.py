# -*- coding: utf-8 -*-
"""Setting default Components."""

from zope import component
from zope import interface

from raptus.article.core import interfaces


def SetDefaults(object, event):
    """Sets the default components defined by the registered adapters
    providing IDefaultComponents.
    """
    providers = component.getAdapters((object,), interfaces.IDefaultComponents)
    for name, provider in providers:
        for comp in provider.getComponents():
            interface.alsoProvides(object, comp.interface)
    object.reindexObject(idxs=['object_provides'])
