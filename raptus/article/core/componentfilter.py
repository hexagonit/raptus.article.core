from zope import interface, component

from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces.browser import IBrowserView
from plone.app.layout.viewlets import interfaces as viewletmanagers

from raptus.article.core import interfaces

ORDERED_VIEWLET_MANAGERS = (
            ('plone.htmlhead', viewletmanagers.IHtmlHead),
            ('plone.htmlhead.links', viewletmanagers.IHtmlHeadLinks),
            ('plone.portaltop', viewletmanagers.IPortalTop),
            ('plone.portalheader', viewletmanagers.IPortalHeader),
            ('plone.contentviews', viewletmanagers.IContentViews),
            ('plone.abovecontent', viewletmanagers.IAboveContent),
            ('plone.abovecontenttitle', viewletmanagers.IAboveContentTitle),
            ('plone.documentactions', viewletmanagers.IDocumentActions),
            ('plone.belowcontenttitle', viewletmanagers.IBelowContentTitle),
            ('plone.abovecontentbody', viewletmanagers.IAboveContentBody),
            ('plone.belowcontentbody', viewletmanagers.IBelowContentBody),
            ('plone.belowcontent', viewletmanagers.IBelowContent),
            ('plone.portalfooter', viewletmanagers.IPortalFooter)
    )


class ComponentFilter(object):
    """Filters and sorts components based on the registration of their
    viewlets."""
    interface.implements(interfaces.IComponentFilter)
    component.adapts(interface.Interface, IHTTPRequest, IBrowserView)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def filter(self, components):
        """ Returns a filtered list of components
        """

        # prevent crashing if passing in an empty list of components
        if not components:
            return []

        # temporary provide all interfaces of the registered components
        notprovided = self.provide_all_interfaces(components)

        # get a list of all viewlets, ordered by their viewlet manager
        order = self.get_ordered_viewlets()

        # no longer provide the interfaces previously set
        self.unprovide_notprovided(notprovided)

        components = [(name, comp) for name, comp in components if comp.viewlet in order]
        components.sort(lambda x, y: cmp(order.index(x[1].viewlet), order.index(y[1].viewlet)))
        return components

    def get_ordered_viewlets(self):
        """Return all viewlets ordered by their viewlet manager."""
        order = []
        for name, iface in ORDERED_VIEWLET_MANAGERS:
            manager = self.get_viewlet_manager(name, iface)
            manager.update()
            for viewlet in manager.viewlets:
                if hasattr(viewlet, '__name__'):
                    order.append(viewlet.__name__)
        return order

    def get_viewlet_manager(self, name, iface):
        """Get viewlet managers with a Multi-Adapter lookup."""

        # viewlet managers require a view object for adaptation
        view = component.getMultiAdapter((self.context, self.request),
                                         name=u'view')

        return component.getMultiAdapter((self.context, self.request, view),
                                         iface, name=name)

    def provide_all_interfaces(self, components):
        """Make context provide all interfaces of all registered components.
        Return those interfaces that were not provided (for later use)."""
        notprovided = []
        for name, comp in components:
            if not comp.interface.providedBy(self.context):
                notprovided.append(comp.interface)
                interface.alsoProvides(self.context, comp.interface)
        return notprovided

    def unprovide_notprovided(self, interfaces):
        """Make context no longer provide passed interfaces."""
        for iface in interfaces:
            interface.noLongerProvides(self.context, iface)
