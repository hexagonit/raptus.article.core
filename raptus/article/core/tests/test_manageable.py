# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import mock
import unittest2 as unittest


class TestBuildAnchor(unittest.TestCase):
    """Test edge cases of Manageable.build_anchor()."""

    def makeManageable(self, component=''):
        """Prepares an instance of Manageable."""
        from raptus.article.core.manageable import Manageable
        context = mock.Mock(spec='absolute_url portal_membership'.split())
        manageable = Manageable(context)
        manageable.component = component
        return manageable

    def test_no_component(self):
        """Return only item_id if self.component is not set."""
        manageable = self.makeManageable()
        self.assertEquals('foo', manageable.build_anchor('foo'))




class TestGetPositionsIntegration(RACoreIntegrationTestCase):
    """Test integration Plone's API for retrieving position
    in parent.
    """

    def makeManageable(self, article=None):
        """Prepares an instance of Manageable."""
        from raptus.article.core.interfaces import IManageable
        if not article:
            article = self.portal.article
        return IManageable(article)

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_catalog_api(self):
        """Test if we correctly use CatalogTool's API for retrieving
        object's position in parent.
        """
        # get number of items in self.portal and use that to
        # calculate the expected positions of newly created content
        # deduct -1 because position values start with 0
        position = len(self.portal.getChildNodes()) - 1

        # create some articles
        self.portal.invokeFactory('Article', 'article2')
        self.portal.invokeFactory('Article', 'article3')

        manageable = self.makeManageable()

        objects = [
            self.portal.article2,
            self.portal.article3,
            ]

        self.assertEquals([position + 1, position + 2], manageable.get_positions(objects))


class TestManageableFlagsIntegration(RACoreIntegrationTestCase):
    """Test how flags are set in __init__() of Manageable."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_sort_flag_based_on_permission(self):
        """Test if sort flag is correctly set based on
        ModifyPortalContent permission.
        """
        from raptus.article.core.interfaces import IManageable

        # this article provides IOrderedContainer by default,
        # so we can focus on testing permissions
        article = self.portal.article

        # Logged in as Manager -> sorting is allowed because
        # we have ModifyPortalContent permission
        self.assertEquals(IManageable(article).sort, True)

        # Logout -> sorting is rejected
        logout()
        self.assertEquals(IManageable(article).sort, False)

    @mock.patch('raptus.article.core.manageable.IOrderedContainer')
    def test_sort_flag_based_on_interface(self, ordered):
        """Test if sort flag is correctly set based on
        IOrderedContainer interface.
        """
        from raptus.article.core.interfaces import IManageable

        # We are logged in as Manager by default, so we can focus on testing
        # setting sort flag based on IOrderedContainer interface
        article = self.portal.article

        # article provides IOrderedContainer by default
        self.assertEquals(IManageable(article).sort, True)

        # simulate an article that does not provide IOrderedContainer
        ordered.providedBy.return_value = False
        self.assertEquals(IManageable(article).sort, False)

    def test_delete_flag(self):
        """Test if delete flag is correctly set."""
        from raptus.article.core.interfaces import IManageable
        article = self.portal.article

        # Logged in as Manager -> deleting is allowed because
        # we have DeleteObjects permission
        self.assertEquals(IManageable(article).delete, True)

        # Logout -> deleting is rejected
        logout()
        self.assertEquals(IManageable(article).delete, False)


class TestGetListIntegration(RACoreIntegrationTestCase):
    """Integration test for Manageable.getList()."""

    def makeManageable(self, article=None):
        """Prepares an instance of Manageable."""
        from raptus.article.core.interfaces import IManageable
        if not article:
            article = self.portal.article
        return IManageable(article)

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_getList_full(self):
        """Test full result dictionary that getList() returns
        for a Folder inside an Article.
        """

        # add sub-content to our test article
        self.portal.article.invokeFactory('Folder', 'subfolder')

        # get Catalog brains of test content
        catalog = getToolByName(self.portal, 'portal_catalog')
        brains = catalog(sort_on='getObjPositionInParent',
                         path={'query': '/'.join(self.portal.article.getPhysicalPath()),
                               'depth': 1},)

        # get list to test it
        manageable = self.makeManageable(self.portal.article)
        results = manageable.getList(brains, 'raptus.related')
        self.assertEquals(len(results), 1)

        item = results[0]
        self.assertEquals(len(item.keys()), 11)

        self.assertEquals(item['up'], None)
        self.assertEquals(item['down'], None)
        self.assertEquals(item['anchor'], 'raptus.relatedsubfolder')
        self.assertEquals(item['id'], 'subfolder')
        self.assertEquals(item['brain'], brains[0])
        self.assertEquals(item['obj'], self.portal.article.subfolder)

        self.assertEquals(item['edit'], 'http://nohost/plone/article/subfolder/edit')
        self.assertEquals(item['view'], 'http://nohost/plone/article/subfolder/view')
        self.assertEquals(item['delete'], 'http://nohost/plone/article/subfolder/delete_confirmation')

        self.assertEquals(item['hide'], None)
        self.assertEquals(item['show'],
            'http://nohost/plone/article/@@article_showhideitem?' +
            'anchor=raptus.relatedsubfolder&action=show&uid=%s&component=raptus.related'
            % self.portal.article.subfolder.UID())

    def test_getList_up_down(self):
        """Test up/down URLs returned by getList() for Images contained
        in an Article.
        """
        # allow adding Images to Articles
        portal_types = getToolByName(self.portal, 'portal_types')
        types = list(portal_types.Article.allowed_content_types)
        types.append('Image')
        portal_types.Article.allowed_content_types = tuple(types)

        # add sub-content to our test article
        self.portal.article.invokeFactory('Image', 'Image1')
        self.portal.article.invokeFactory('Image', 'Image2')
        self.portal.article.invokeFactory('Image', 'Image3')

        # get Catalog brains of test content
        catalog = getToolByName(self.portal, 'portal_catalog')
        brains = catalog(sort_on='getObjPositionInParent',
                         path={'query': '/'.join(self.portal.article.getPhysicalPath()),
                               'depth': 1},)

        # get list to test it
        manageable = self.makeManageable(self.portal.article)
        results = manageable.getList(brains, 'raptus.related')
        self.assertEquals(len(results), 3)

        item = results[1]
        self.assertEquals(item['up'],
            'http://nohost/plone/article/article_moveitem?anchor=raptus.relatedImage2&delta=-1&item_id=Image2')
        self.assertEquals(item['down'],
            'http://nohost/plone/article/article_moveitem?anchor=raptus.relatedImage2&delta=1&item_id=Image2')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
