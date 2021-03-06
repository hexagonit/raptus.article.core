# -*- coding: utf-8 -*-
"""Manage Items in Artcles: move, show/hide, etc."""

from OFS.interfaces import IOrderedContainer
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import getObjPositionInParent
from raptus.article.core.interfaces import IManageable
from zope import component
from zope import interface


class Manageable(object):
    """Provides information dict used for the manage macro for objects
    which are manageable.
    """
    interface.implements(IManageable)
    component.adapts(interface.Interface)

    def __init__(self, context):
        self.pos = []
        self.component = ''
        self.context = context
        self.mship = getToolByName(self.context, 'portal_membership')
        self.delete = self.mship.checkPermission(permissions.DeleteObjects, self.context) or False
        self.sort = (IOrderedContainer.providedBy(self.context)
                    and self.mship.checkPermission(permissions.ModifyPortalContent, self.context)) or False

    def getList(self, brains, component=''):
        """Returns a list of dicts holding the specific links for viewing,
        editing, sorting and deleting the obj.

        :param brains: items in Article that are manageable
        :type brains: portal_catalog brains
        :param component: component for which this list is being built
        :type component: string
        :returns: list of items along with their metadata and their manageable links
        :rtype: list of dicts
        """
        items = []

        self.component = component
        self.len = len(brains)
        self.pos = self.get_positions(brain.getObject() for brain in brains)

        # iterate through objects and set dict values we need
        # in the template
        for i, brain in enumerate(brains):
            obj = brain.getObject()

            # get a list of components for which this item is shown
            try:
                components = obj.Schema()['components'].get(obj)
            except:
                components = []

            # Build URL anchor string that is used in constructing URLs
            anchor = self.build_anchor(brain.id)

            item = {
                    'obj': obj,
                    'brain': brain,
                    'id': brain.id,
                    'anchor': anchor,
                    'up': self.build_url_up(i, brain, anchor),
                    'down': self.build_url_down(i, brain, anchor),
                    'view': '%s/view' % brain.getURL(),
                    'edit': self.build_url_edit(brain),
                    'delete': self.build_url_delete(brain),
                    'show': self.build_url_show_hide(components, brain, 'show'),
                    'hide': self.build_url_show_hide(components, brain, 'hide'),
                   }
            items.append(item)

        return items

    def get_positions(self, objects):
        """Returns a list of objPositionInParent values for passed objects."""
        return [getObjPositionInParent(obj)() for obj in objects]

    def build_anchor(self, item_id):
        """Build URL anchor id that will be used in URLs for
        moving/deleting/showing/hiding items on listings.
        """
        return '%s%s' % (self.component, item_id)

    def build_url_up(self, i, brain, anchor):
        """Builds an URL that can be later called to move
        this item up on the list of items contained in an article.
        """
        # sorting is not enabled/allowed
        if not self.sort:
            return None

        # this is the first item on the list, it cannot be moved higher
        if i == 0:
            return None

        mapping = dict(
            item_id=brain.id,
            anchor=anchor,
            url=self.context.absolute_url(),
            delta=self.pos[(i - 1)] - self.pos[i]
            )

        return '%(url)s/article_moveitem?anchor=%(anchor)s&delta=%(delta)s&item_id=%(item_id)s' % mapping

    def build_url_down(self, i, brain, anchor):
        """Builds an URL that can be later called to move
        this item down on the list of items contained in an article.
        """
        # sorting is not enabled/allowed
        if not self.sort:
            return None

        # this is the last item on the list, it cannot be moved lower
        if i == (self.len - 1):
            return None

        mapping = dict(
            item_id=brain.id,
            anchor=anchor,
            url=self.context.absolute_url(),
            delta=self.pos[(i + 1)] - self.pos[i]
            )

        return '%(url)s/article_moveitem?anchor=%(anchor)s&delta=%(delta)s&item_id=%(item_id)s' % mapping

    def build_url_edit(self, brain):
        """Builds an URL that can be used to edit this item."""
        # User does not have permissions to modify this item
        if not self.mship.checkPermission(permissions.ModifyPortalContent, brain.getObject()):
            return None
        return '%s/edit' % brain.getURL()

    def build_url_delete(self, brain):
        """Builds an URL that can be used to delete this item."""
        # User does not have permissions to delete items in this container
        if not self.delete:
            return None

        # User does not have permissions to delete this item
        if not self.mship.checkPermission(permissions.DeleteObjects, brain.getObject()):
            return None

        # TODO: why do we need both of the above, shouldn't it be enough only to check
        # for delete permission on the item and not also on the container?

        return '%s/delete_confirmation' % brain.getURL()

    def build_url_show_hide(self, components, brain, action):
        """Builds an URL that can be used to show this item."""
        # This is a generic getList request, there is no specific component
        if not self.component:
            return None

        # User does not have permissions to modify this item
        if not self.mship.checkPermission(permissions.ModifyPortalContent, brain.getObject()):
            return None

        # if item is already shown we don't need the 'show' link
        if action == 'show' and self.component in components:
            return None

        # if item is already hidden we don't need the 'hide' link
        if action == 'hide' and self.component not in components:
            return None

        mapping = dict(
            item_id=brain.id,
            anchor=self.build_anchor(brain.id),
            action=action,
            uid=brain.UID,
            component=self.component,
            url=self.context.absolute_url(),
            )

        return'%(url)s/@@article_showhideitem?anchor=%(anchor)s&action=%(action)s&uid=%(uid)s&component=%(component)s' % mapping
