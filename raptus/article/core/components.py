from zope import interface, component

from raptus.article.core import interfaces

class Components(object):
    """ Provides information about available and active components
    """
    interface.implements(interfaces.IComponents)
    component.adapts(interfaces.IArticle)
    
    def __init__(self, context):
        self.context = context
    
    def getComponents(self):
        """ Returns a list of available components
        """
        return [(name, comp) for name, comp in component.getAdapters((self.context,), interfaces.IComponent)]
        
    def activeComponents(self):
        """ Returns a list of the active components
        """
        return [(name, comp) for name, comp in self.getComponents() if comp.interface.providedBy(self.context)]
