## Script (Python) "article_moveitem"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=item_id,delta,anchor
##title=
##
context.folder_moveitem(item_id, delta)

return context.REQUEST.RESPONSE.redirect('%s#%s' % (context.absolute_url(), anchor))
