# -*- coding: utf-8 -*-
"""Support for showing/hiding Items in Article."""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from raptus.article.core import interfaces
from zope.component import queryAdapter


class ShowHideItem(BrowserView):
    """Shows/hides an item in a component."""

    def __call__(self, action, uid, component, anchor=''):
        """Handles showing/hiding an item in a certain component.

        :param action: show or hide
        :type action: string
        :param uid: UID of item to show/hide
        :type uid: string
        :param component: Name of component in which to show/hide this item
        :type component: string
        :param anchor: URL anchor to which to redirect when finished
        :type anchor: string
        """
        self.redirect(anchor)
        if not queryAdapter(self.context, interface=interfaces.IComponent, name=component):
            return
        item = self.get_item(uid)
        if not item:
            return
        try:
            components = self.get_components(item)
        except:
            return
        if action == 'show' and not component in components:
            self.set_item_show(item, component, components)
            item.reindexObject()
        if action == 'hide' and component in components:
            self.set_item_hide(item, component, components)
            item.reindexObject()

    def set_item_show(self, item, component, components):
        """Show this item in this component by adding this component
        to the 'components' field of this item.

        :param item: item in Article that is to be shown
        :type item: content object
        :param component: name of component in which this item is to be shown
        :type component: string
        :param components: names of components in which this item is already shown
        :type components: tuple of strings
        """
        components = components + [component, ]
        item.Schema()['components'].set(item, components)

    def set_item_hide(self, item, component, components):
        """Hide this item in this component by removing this component
        to the 'components' field of this item.

        :param item: item in Article that is to be shown
        :type item: content object
        :param component: name of component in which this item is to be hidden
        :type component: string
        :param components: names of components in which this item is shown
        :type components: tuple of strings
        """
        components = [c for c in components if not c == component]
        item.Schema()['components'].set(item, components)

    def get_components(self, item):
        """Return components set in item's components field.

        :param item: item in Article that has a field 'components'
        :type item: content object
        :returns: names of components in which this item is shown
        :rtype: tuple of strings
        """
        components = item.Schema()['components'].get(item)
        return list(components)

    def get_item(self, uid):
        """Get's an item by it's UID.

        :param uid: UID of the item that is to be fetched
        :type uid: string
        :returns: item in Article
        :rtype: content object
        """
        catalog = getToolByName(self.context, 'uid_catalog')
        results = catalog(UID=uid)
        if not len(results):
            return None
        return results[0].getObject()

    def redirect(self, anchor):
        """Redirects user back to where he was: Context + item's anchor.

        :param anchor: URL anchor to which to redirect
        :type anchor: string
        """
        self.request.RESPONSE.redirect('%s#%s' % (self.context.absolute_url(), anchor))
