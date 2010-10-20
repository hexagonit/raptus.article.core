from Products.CMFCore.utils import getToolByName

DEPENDENCIES = (
    'DynamicHeader',
)

def install(context):
    """ Adds required catalog indexes, makes articles linkable in kupu and installs dependencies
    """
    if context.readDataFile('raptus.article.core_install.txt') is None:
        return
    portal = context.getSite()
    
    catalog = getToolByName(portal, 'portal_catalog')
    if 'component' not in catalog.indexes():
        catalog.addIndex('component', 'KeywordIndex', None)
    
    inst = getToolByName(portal, 'portal_quickinstaller')
    for prod in DEPENDENCIES:
        if inst.isProductInstallable(prod):
            if not inst.isProductInstalled(prod):
                inst.installProduct(prod)
            else:
                inst.reinstallProducts(prod)
                
    try: # try updating kupu library tool if available
        kupu = getToolByName(portal, 'kupu_library_tool')
        linkable = list(kupu.getPortalTypesForResourceType('linkable'))
        if 'Article' not in linkable:
            linkable.append('Article')
            kupu.updateResourceTypes(({'resource_type' : 'linkable',
                                       'old_type'      : 'linkable',
                                       'portal_types'  :  linkable},))
    except:
        pass