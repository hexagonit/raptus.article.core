# -*- coding: utf-8 -*-
"""Filtering and sorting a list of Components."""

import logging

from zope import component
from zope import interface
from zope.component.interfaces import ComponentLookupError
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.http import IHTTPRequest

from plone.app.layout.viewlets import interfaces as viewletmanagers

from raptus.article.core import interfaces

logger = logging.getLogger('raptus.article.core')

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
    viewlets.
    """
    interface.implements(interfaces.IComponentFilter)
    component.adapts(interface.Interface, IHTTPRequest, IBrowserView)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.view = view

    def filter(self, components):
        """Returns a filtered list of components.

        :param components: (name, component) pairs of article components and their names
        :type components: list
        :returns: sorted (name, component) pairs of article components and their names
        :rtype: list of tuples
        """

        # prevent crashing if passing in an empty list of components
        if not components:
            return []

        # temporary provide all interfaces of the registered components
        notprovided = self.provide_all_interfaces(components)

        # get a list of all viewlets, ordered by their viewlet manager
        order = self.get_ordered_viewlets()

        # no longer provide the interfaces previously set
        for iface in notprovided:
            interface.noLongerProvides(self.context, iface)

        # compile a list of components whose viewlets are present in the list
        # of ordered viewlets
        components = [(name, comp) for name, comp in components
                                                  if comp.viewlet in order]

        # sort components based on their position in 'order'
        components = self.sort_components(components, order)
        return components

    def sort_components(self, components, order):
        """Sort components based on their position in 'order'. If
        there is an error while sorting, return unsorted list.

        :param components: (name, component) pairs of article components and their names
        :type components: list of tuples
        :param order: viewlet names, sorted based on their position in site layout
        :type order: list of strings
        :returns: sorted (name, component) pairs
        :rtype: list of tuples
        """
        # 'components' is a list of tuples: (<comp name>, <comp object>)
        # 'order' is a list of viewlet names
        # sort by comparing items in 'order' to return values of
        # <comp object>.viewlet
        components.sort(key=lambda x: order.index(x[1].viewlet))
        return components

    def get_ordered_viewlets(self):
        """Return all viewlets ordered by their viewlet manager.

        :returns: viewlet names, sorted based on their position in site layout
        :rtype: list of strings
        """
        order = []
        for name, iface in ORDERED_VIEWLET_MANAGERS:

            # get viewlet manager and run update() so it registers
            # it's viewlets
            try:
                manager = self.get_viewlet_manager(name, iface)
            except ComponentLookupError:
                logger.warning("Couldn't find '%s' viewlet manager." % name)
                continue
            manager.update()

            # go through all manager's viewlets and add them to list of
            # ordered viewlets
            for viewlet in manager.viewlets:
                if not hasattr(viewlet, '__name__'):
                    logger.warning("Viewlet '%s' does not have a __name__, so \
                                    it cannot be added it to the list of \
                                    ordered viewlets." % viewlet)
                    continue
                order.append(viewlet.__name__)
        return order

    def get_viewlet_manager(self, name, iface):
        """Get viewlet managers with a Multi-Adapter lookup.

        :param name: viewlet manager's name
        :type name: strings
        :param name: viewlet manager's interface
        :type name: Interface
        :returns: ViewletManager of specified interface and name
        :rtype: ViewletManager
        """

        # viewlet managers require a view object for adaptation
        view = component.getMultiAdapter((self.context, self.request),
                                         name=u'view')
        return component.getMultiAdapter((self.context, self.request, view),
                                         iface, name=name)

    def provide_all_interfaces(self, components):
        """Make context provide all interfaces of all registered components.
        Return those interfaces that were not provided (for later use).

        :param components: (name, component) pairs of article components and their names
        :type components: list of tuples
        :returns: Interfaces that were previously not provided (for later use in the main method)
        :rtype: list of Interfaces
        """
        notprovided = []
        for name, comp in components:
            if not comp.interface.providedBy(self.context):
                notprovided.append(comp.interface)
                interface.alsoProvides(self.context, comp.interface)
        return notprovided
