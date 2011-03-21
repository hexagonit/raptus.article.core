from zope.component import getMultiAdapter

from plone.app.contentmenu.menu import FactoriesMenu as BaseFactoriesMenu
from plone.app.contentmenu.menu import _allowedTypes

from Products.CMFPlone.interfaces.constrains import IConstrainTypes
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone import PloneMessageFactory as _p

class FactoriesMenu(BaseFactoriesMenu):
    
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = BaseFactoriesMenu.getMenuItems(self, context, request)
        
        factories_view = getMultiAdapter((context, request), name='folder_factories')

        haveMore = False
        include = None

        addContext = factories_view.default_page_add_context()
        if not addContext:
            return results
        allowedTypes = _allowedTypes(request, addContext)

        constraints = IConstrainTypes(addContext, None)
        if constraints is not None:
            include = constraints.getImmediatelyAddableTypes()
            if len(include) < len(allowedTypes):
                haveMore = True
                
        results.append({'title'       : _p(u'folder_add_to_default_page', default=u'Add to default page'),
                        'description' : _p(u'Add content to the default page'),
                        'action'      : None,
                        'selected'    : False,
                        'icon'        : None,
                        'extra'       : {'id': 'add-to-default', 'separator': 'actionSeparator', 'class': ''},
                        'submenu'     : None,
                        })

        results += factories_view.default_page_addable_types(include=include)

        if haveMore:
            url = '%s/folder_factories' % (addContext.absolute_url(),)
            results.append({ 'title'       : _p(u'folder_add_more', default=u'More\u2026'),
                             'description' : _p(u'Show all available content types'),
                             'action'      : url,
                             'selected'    : False,
                             'icon'        : None,
                             'extra'       : {'id': 'more', 'separator': None, 'class': ''},
                             'submenu'     : None,
                            })

        constraints = ISelectableConstrainTypes(addContext, None)
        if constraints is not None:
            if constraints.canSetConstrainTypes() and constraints.getDefaultAddableTypes():
                url = '%s/folder_constraintypes_form' % (addContext.absolute_url(),)
                results.append({'title'       : _p(u'folder_add_settings', default=u'Restrictions\u2026'),
                                'description' : _p(u'title_configure_addable_content_types', default=u'Configure which content types can be added here'),
                                'action'      : url,
                                'selected'    : False,
                                'icon'        : None,
                                'extra'       : {'id': 'settings', 'separator': None, 'class': ''},
                                'submenu'     : None,
                                })

        return results