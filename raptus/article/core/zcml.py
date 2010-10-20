import os

from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Path
from zope.configuration.fields import PythonIdentifier
from zope.security.zcml import Permission
from zope import interface, component

from zope.component.zcml import adapter
from Products.Five.viewlet.metaconfigure import viewletDirective
from Products.Five.browser.metaconfigure import resource  

from raptus.article.core import interfaces

class IComponentDirective(interface.Interface):
    """Register a component to be used by articles
    """

    name = PythonIdentifier(
        title=u'Name',
        description=u"",
        required=True)

    component = GlobalObject(
        title=u'Component',
        description=u'',
        required=True)
    
    viewlet = GlobalObject(
        title=u'Viewlet',
        description=u'',
        required=True)

    manager = GlobalObject(
        title=u'Viewlet manager',
        description=u'',
        required=True)

    selection = GlobalObject(
        title=u'ComponentSelection',
        description=u'For which object this component may be selected.',
        default=None,
        required=False)

    image = Path(
        title=u'Image',
        description=u"If not specified the one set in the component is registered.",
        required=False)

    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to view the viewlet.",
        default='zope.Public',
        required=True)


def registerComponent(_context, name, component, viewlet, manager, 
                      selection=None, image=None, permission="zope.Public"):
    """ Register a component to be used by articles
    """
    adapter(_context, [component], interfaces.IComponent, name=name, for_=[interfaces.IArticle])
    if selection:
        adapter(_context, [component], interfaces.IComponentSelection, name=name, for_=[selection])
        
    viewletDirective(_context, component.viewlet, permission, for_=component.interface, manager=manager, class_=viewlet, view=interfaces.IArticleView)
    
    if not image:
        path = os.path.abspath(str(_context.path(component.image.replace('++resource++', ''))))
        if os.path.isfile(path):
            image = path
    if image:
        resource(_context, component.image.replace('++resource++', ''), image=image)
