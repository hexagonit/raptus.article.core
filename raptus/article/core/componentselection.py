# -*- coding: utf-8 -*-
"""Archetypes vocabulary and widget for selecting Components on an item."""

from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent

from Products.Archetypes.interfaces import IFieldDefaultProvider
from Products.Archetypes.Widget import MultiSelectionWidget
from Products.CMFPlone.FactoryTool import TempFolder

from zope import component
from zope import interface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm

from raptus.article.core.interfaces import IArticle
from raptus.article.core.interfaces import IComponentFilter
from raptus.article.core.interfaces import IComponentSelection


class ComponentSelectionVocabulary(object):
    """Archetypes vocabulary for component selection field."""
    interface.implements(IVocabularyFactory)

    def __call__(self, context):

        container = self.get_containing_article(context)
        if not container:
            return []

        components = self.get_selectable_components(context)
        view = component.getMultiAdapter((container, context.REQUEST), name=u'components')
        sorter = component.getMultiAdapter((container, context.REQUEST, view), IComponentFilter)
        components = sorter.filter(components)
        items = []
        for name, comp in components:
            items.append(SimpleTerm(name, None, comp.title))
        return items

    def get_containing_article(self, context):
        """Get the Article that this Item is contained in."""
        container = aq_parent(context)

        # if this item is just being created we need to move higher
        # up the inheritance tree to reach it's actual parent Article
        if context.isTemporary() and isinstance(container, TempFolder):
            container = aq_parent(aq_parent(container))

        # return False for containers that are not Articles
        if not IArticle.providedBy(container):
            return False

        return container

    def get_selectable_components(self, context):
        """Returns a list of selectable components."""
        return [(name, comp) for name, comp in component.getAdapters((context,), IComponentSelection)]


class ComponentSelectionWidget(MultiSelectionWidget):
    _properties = MultiSelectionWidget._properties.copy()
    _properties.update({
        'format': "checkbox",
        })
    security = ClassSecurityInfo()

    security.declarePublic('isVisible')
    def isVisible(self, instance, mode='view'):
        """Check if we are contained in an Article."""
        container = aq_parent(instance)
        if IArticle.providedBy(container):
            return 'visible'
        return 'invisible'


class ComponentSelectionDefault(object):
    """Archetypes default component selection for fields using component
    selection vocabulary.
    """
    component.adapts(interface.Interface)
    interface.implements(IFieldDefaultProvider)
    def __init__(self, context):
        self.context = context
    def __call__(self):
        vocabulary = component.getUtility(IVocabularyFactory, name=u'componentselectionvocabulary')
        return [term.token for term in vocabulary(self.context)]
