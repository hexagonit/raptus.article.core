from Acquisition import aq_inner

from zope import interface, component

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

from plone.memoize.instance import memoize

from raptus.article.core import RaptusArticleMessageFactory as _
from raptus.article.core import interfaces

class Components(BrowserView):
    """Component selection
    """

    template = ViewPageTemplateFile('components.pt')
    
    def __call__(self):
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
        try:
            context = aq_inner(self.context)
            components = interfaces.IComponents(context).getComponents()
            active = self.request.form.get('form.components', ())
            for name, component in components:
                if name in active:
                    interface.alsoProvides(context, component.interface)
                elif component.interface.providedBy(context):
                    interface.noLongerProvides(context, component.interface)
        except:
            return False
        return True
    
    @property
    @memoize
    def components(self):
        context = aq_inner(self.context)
        components = interfaces.IComponents(context).getComponents()
        sorter = component.getMultiAdapter((context, self.request, self), interfaces.IComponentFilter)
        components = sorter.filter(components)
        items = []
        for name, comp in components:
            items.append({'name' : name,
                          'title' : comp.title,
                          'description' : comp.description,
                          'image' : comp.image,
                          'selected' : comp.interface.providedBy(context)})
        return items