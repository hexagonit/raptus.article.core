# -*- coding: utf-8 -*-
"""The `raptus.related` Component that comes bundled with this
package by default."""

from zope import interface, component

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces


class IRelated(interface.Interface):
    """Marker interface for the related items viewlet."""


class Component(object):
    """Component which lists the related items of an article."""
    interface.implements(interfaces.IComponent)
    component.adapts(interfaces.IArticle)

    title = _(u'Related content')
    description = _(u'List of related content of the article.')
    image = '++resource++related.gif'
    interface = IRelated
    viewlet = 'raptus.article.related'

    def __init__(self, context):
        self.context = context


class Viewlet(ViewletBase):
    """Viewlet listing the related items of the article."""
    index = ViewPageTemplateFile('related.pt')

    @property
    @memoize
    def related(self):
        plone = component.getMultiAdapter((self.context, self.request), name=u'plone')
        use_view_action = self.get_types_that_use_view_action(self.context)
        related = self.context.computeRelatedItems()
        items = []
        for obj in related:
            url = obj.portal_type in use_view_action and '%s/view' or '%s'
            item = {'id': obj.getId(),
                    'title': obj.Title(),
                    'description': obj.Description(),
                    'url': url % obj.absolute_url(),
                    'icon': plone.getIcon(obj).url}
            items.append(item)
        return items

    def get_types_that_use_view_action(self, context):
        """Returns a list of content-types that use '/view' suffix
        in listings."""
        portal_properties = getToolByName(context, 'portal_properties')
        site_properties = portal_properties.site_properties
        return site_properties.get('typesUseViewActionInListings', ())


class RelatedItemsViewlet(ViewletBase):
    """Overrides the default related items viewlet for articles."""
    def index(self):
        return ''
