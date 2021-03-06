# -*- coding: utf-8 -*-
"""Activating/deactivating Components."""

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.memoize.instance import memoize
from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces
from zope import interface, component


class Components(BrowserView):
    """A @@components view for activating/deactivating Components."""

    template = ViewPageTemplateFile('components.pt')

    def __call__(self):
        """Handles StatusMessages and redirect logic.

        :returns: component.pt template or redirects to Article's absolute URL
        :rtype: Five template or response redirect
        """
        if self.request.get('form.submitted', False) or self.request.get('form.view', False):
            statusmessage = IStatusMessage(self.request)
            if self._save():
                statusmessage.addStatusMessage(_(u'Components saved successfully'), u'info')
            else:
                statusmessage.addStatusMessage(_(u'Saving components failed'), u'error')
        if self.request.get('form.view', False):
            return self.request.RESPONSE.redirect(self.context.absolute_url())
        return self.template()

    def _save(self):
        """Save user's selection of active components.

        :returns: True if saving was successful, False if it was not
        :rtype: Boolean
        """
        try:
            context = aq_inner(self.context)
            components = interfaces.IComponents(context).getComponents()
            active = self.request.form.get('form.components', ())
            for name, comp in components:
                if name in active:  # activate component
                    interface.alsoProvides(context, comp.interface)
                else:  # deactivate component
                    interface.noLongerProvides(context, comp.interface)
        except:
            return False
        return True

    @property
    @memoize
    def components(self):
        """Return a list of dicts containing information about components.

        :returns: Information about components (name, title, description, image and active/inactive)
        :rtype: list of dicts
        """
        context = aq_inner(self.context)
        components = interfaces.IComponents(context).getComponents()
        sorter = component.getMultiAdapter((context, self.request, self), interfaces.IComponentFilter)
        components = sorter.filter(components)
        items = []
        for name, comp in components:
            items.append({'name': name,
                          'title': comp.title,
                          'description': comp.description,
                          'image': comp.image,
                          'selected': comp.interface.providedBy(context)})
        return items
