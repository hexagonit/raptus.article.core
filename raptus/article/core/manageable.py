from OFS.interfaces import IOrderedContainer
from zope import interface, component

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.CatalogTool import getObjPositionInParent

from raptus.article.core.interfaces import IManageable

class Manageable(object):
    """ Provider information dict used for the manage macro for objects which are manageable
    """
    interface.implements(IManageable)
    component.adapts(interface.Interface)
    
    def __init__(self, context):
        self.context = context
        self.mship = getToolByName(self.context, 'portal_membership')
        self.sort = IOrderedContainer.providedBy(self.context) and self.mship.checkPermission(permissions.ModifyPortalContent, self.context)
        self.sort_url = '%s/article_moveitem?anchor=%%s&delta=%%s&item_id=%%s' % self.context.absolute_url()
        self.show_hide_url = '%s/@@article_showhideitem?anchor=%%s&action=%%s&uid=%%s&component=%%s' % self.context.absolute_url()
        self.delete = self.mship.checkPermission(permissions.DeleteObjects, self.context)
    
    def getList(self, brains, component=''):
        """
        Returns a list of dicts holding the specific links for viewing, editing, sorting and
        deleting and the obj.
        """
        items = []
        i = 0
        l = len(brains)
        pos = [getObjPositionInParent(brain.getObject())() for brain in brains]
        for brain in brains:
            obj = brain.getObject()
            try:
                components = obj.Schema()['components'].get(obj)
            except:
                components = []
            modify = self.mship.checkPermission(permissions.ModifyPortalContent, obj)
            item = {'obj': obj,
                    'brain': brain,
                    'id': brain.id,
                    'anchor': '%s%s' % (component, brain.id),
                    'up': self.sort and i > 0 and self.sort_url % ('%s%s' % (component, brain.id), pos[(i-1)] - pos[i], brain.id) or None,
                    'down': self.sort and i < l - 1 and self.sort_url % ('%s%s' % (component, brain.id), pos[(i+1)] - pos[i], brain.id) or None,
                    'view': '%s/view' % brain.getURL(),
                    'edit': modify and '%s/edit' % brain.getURL() or None,
                    'delete': self.delete and self.mship.checkPermission(permissions.DeleteObjects, obj) and '%s/delete_confirmation' % brain.getURL() or None,
                    'show': modify and component and not component in components and self.show_hide_url % ('%s%s' % (component, brain.id), 'show', brain.UID, component) or None,
                    'hide': modify and component and component in components and self.show_hide_url % ('%s%s' % (component, brain.id), 'hide', brain.UID, component) or None}
            items.append(item)
            i += 1
        return items
