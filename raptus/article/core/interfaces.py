from zope.interface import Attribute, Interface

class IArticle(Interface):
    """ Marker interface for the article content type
    """

class IArticleView(Interface):
    """ Marker interface for the article view
    """

class IComponents(Interface):
    """ Provides information about available and active components
    """
    
    def getComponents():
        """ Returns a list of available components
        """
        
    def activeComponents():
        """ Returns a list of the active components
        """

class IComponent(Interface):
    """ A component definition
    """
    
    title = Attribute('title', 'User friendly title of the component')
    description = Attribute('description', 'User friendly description of the component')
    image = Attribute('image', 'Descriptive image of the component')
    interface = Attribute('interface', 'The interface the viewlet rendering the component is bound to')
    viewlet = Attribute('viewlet', 'The name of the viewlet rendering the component')

class IComponentFilter(Interface):
    """ Filters and sorts components based on the registration of their viewlets
    """
    
    def filter(components):
        """ Returns a filtered list of components
        """

class IComponentSelection(IComponent):
    """ A component selection registering a component for selection on a content type
    """
    
class IDefaultComponents(Interface):
    """ Provider to define default components on newly created articles
    """
    
    def getComponents():
        """ Returns a list of components which should be activated
        """
        
class IManageable(Interface):
    """ Provider information dict used for the manage macro for objects which are manageable
    """
    
    def getList(brains):
        """
        Returns a list of dicts holding the specific links for viewing, editing, sorting and
        deleting and the obj.
        """
