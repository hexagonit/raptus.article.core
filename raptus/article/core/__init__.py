# -*- coding: utf-8 -*-
"""Main product initializer."""

from Products.Archetypes import atapi
from Products.CMFCore import utils as cmfutils

from raptus.article.core import config

from zope.i18nmessageid import MessageFactory
RaptusArticleMessageFactory = MessageFactory('raptus.article')


def initialize(context):

    # this needs to be here so that module-level functions in article.py
    # are run when Zope starts; 'del article' is here so that pyflakes is happy
    from content import article

    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        cmfutils.ContentInit("%s: %s" % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSION,
            extra_constructors=(constructor,),
            ).initialize(context)
