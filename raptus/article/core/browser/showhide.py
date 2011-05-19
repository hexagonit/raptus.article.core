from zope.component import queryAdapter

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from raptus.article.core import interfaces


class ShowHideItem(BrowserView):
    """Shows/hides an item in a component
    """
    
    def __call__(self, action, uid, component, anchor=''):
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
        to the 'components' field of this item."""
        components = components+[component,]
        item.Schema()['components'].set(item, components)

    def set_item_hide(self, item, component, components):
        """Hide this item in this component by removing this component
        to the 'components' field of this item."""
        components = [c for c in components if not c == component]
        item.Schema()['components'].set(item, components)

    def get_components(self, item):
        """Return components set in item's components field."""
        components = item.Schema()['components'].get(item)
        return list(components)

    def get_item(self, uid):
        """Get's an item by it's UID."""
        catalog = getToolByName(self.context, 'uid_catalog')
        results = catalog(UID=uid)
        if not len(results):
            return None
        return results[0].getObject()

    def redirect(self, anchor):
        """Redirects user back to where he was: Context + item's anchor. """
        self.request.RESPONSE.redirect('%s#%s' % (self.context.absolute_url(), anchor))
