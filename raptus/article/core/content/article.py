"""Definition of the Article content type
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements, classImplements

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    # No multilingual support
    from Products.Archetypes import atapi
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content import folder
from Products.ATContentTypes import ATCTMessageFactory as _at

from raptus.article.core.interfaces import IArticle
from raptus.article.core.config import PROJECTNAME
from raptus.article.core import RaptusArticleMessageFactory as _

ArticleSchema = folder.ATFolderSchema.copy() + atapi.Schema((
        atapi.TextField('text',
            required=False,
            searchable=True,
            storage = atapi.AnnotationStorage(),
            validators = ('isTidyHtmlWithCleanup',),
            default_output_type = 'text/x-html-safe',
            widget = atapi.RichWidget(
                description = '',
                label = _at(u'label_body_text', default=u'Body Text'),
                rows = 25,
                allow_file_upload = zconf.ATDocument.allow_document_upload
            ),
        ),
        atapi.BooleanField('hideTitle',
            required = False,
            languageIndependent = True,
            default = False,
            storage = atapi.AnnotationStorage(),
            schemata = 'settings',
            accessor = 'HideTitle',
            widget = atapi.BooleanWidget(
                description='',
                label = _(u'label_hide_title', default=u'Hide title'),
                visible={'view' : 'hidden',
                         'edit' : 'visible'},
            ),
        ),
        
        atapi.BooleanField('hideDescription',
            required = False,
            languageIndependent = True,
            default = False,
            storage = atapi.AnnotationStorage(),
            schemata = 'settings',
            accessor = 'HideDescription',
            widget = atapi.BooleanWidget(
                description='',
                label = _(u'label_hide_description', default=u'Hide description'),
                visible={'view' : 'hidden',
                         'edit' : 'visible'},
            ),
        ),
    ))

try:
    from Products.DynamicHeader.config import DynamicHeaderMixinSchema
    ArticleSchema = ArticleSchema + DynamicHeaderMixinSchema
except:
    # No dynamic header support
    pass

ArticleSchema['title'].storage = atapi.AnnotationStorage()
ArticleSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ArticleSchema, folderish=True, moveDiscussion=True)
ArticleSchema['relatedItems'].widget.visible = {'edit': 'visible', 'view': 'invisible'}
ArticleSchema.changeSchemataForField('relatedItems', 'default')

class Article(folder.ATFolder):
    """An article"""
    implements(IArticle)
    
    portal_type = "Article"
    schema = ArticleSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    text = atapi.ATFieldProperty('text')
    hideTitle = atapi.ATFieldProperty('hideTitle')
    hideDescription = atapi.ATFieldProperty('hideDescription')
    
    security = ClassSecurityInfo()
    
    security.declarePublic('canSetDefaultPage')
    def canSetDefaultPage(self):
        """
        Override BrowserDefaultMixin because default page stuff doesn't make
        sense for topics.
        """
        return False

try:
    from Products.DynamicHeader.interfaces import IDynamicHeader
    classImplements(Article, IDynamicHeader)
except:
    # No dynamic header support
    pass

atapi.registerType(Article, PROJECTNAME)
