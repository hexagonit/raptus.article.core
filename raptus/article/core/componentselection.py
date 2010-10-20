from Acquisition import aq_parent
from AccessControl import ClassSecurityInfo

from zope import interface, component
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm

from Products.CMFPlone.FactoryTool import TempFolder
from Products.Archetypes.interfaces import IFieldDefaultProvider
from Products.Archetypes.Widget import MultiSelectionWidget

from raptus.article.core import interfaces

class ComponentSelectionVocabulary(object):
    """ Archetypes vocabulary for component selection field
    """
    interface.implements(IVocabularyFactory)
    
    def __call__(self, context):
        container = aq_parent(context)
        if context.isTemporary() and isinstance(container, TempFolder):
            container = aq_parent(aq_parent(container))
        if not interfaces.IArticle.providedBy(container):
            return []
        components = [(name, comp) for name, comp in component.getAdapters((context,), interfaces.IComponentSelection)]
        view = component.getMultiAdapter((container, context.REQUEST), name=u'components')
        sorter = component.getMultiAdapter((container, context.REQUEST, view), interfaces.IComponentFilter)
        components = sorter.filter(components)
        items = []
        for name, comp in components:
            items.append(SimpleTerm(name, None, comp.title))
        return items
    
class ComponentSelectionWidget(MultiSelectionWidget):
    _properties = MultiSelectionWidget._properties.copy()
    _properties.update({
        'format': "checkbox",
        })
    security = ClassSecurityInfo()

    security.declarePublic('isVisible')
    def isVisible(self, instance, mode='view'):
        """ Check if we are contained in an Article
        """
        container = aq_parent(instance)
        if interfaces.IArticle.providedBy(container):
            return 'visible'
        return 'invisible'

class ComponentSelectionDefault(object):
    """ Archetypes default component selection for fields using component selection vocabulary
    """
    component.adapts(interface.Interface)
    interface.implements(IFieldDefaultProvider)
    def __init__(self, context):
        self.context = context
    def __call__(self):
        vocabulary = component.getUtility(IVocabularyFactory, name=u'componentselectionvocabulary')
        return [term.token for term in vocabulary(self.context)]