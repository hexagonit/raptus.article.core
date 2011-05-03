# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import mock
import unittest2 as unittest


class TestGetPositionsIntegration(RACoreIntegrationTestCase):
    """Test integration Plone's API for retrieving position
    in parent."""

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
        object's position in parent."""
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
        ModifyPortalContent permission."""
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
        IOrderedContainer interface."""
        from raptus.article.core.interfaces import IManageable

        # We are logged in as Manager by default, so we can focus on testing
        # setting sort flag based on IOrderedContainer interface
        article = self.portal.article

        # article provides IOrderedContainer by default
        self.assertEquals(IManageable(article).sort, True)

        # simulate an article that does not provide IOrderedContainer
        ordered.providedBy.return_value = False
        self.assertEquals(IManageable(article).sort, False)

    def test_sort_url(self):
        """Test that sort url is correctly compiled."""
        from raptus.article.core.interfaces import IManageable
        article = self.portal.article

        url = IManageable(article).sort_url
        self.assertEquals(url,
            'http://nohost/plone/article/article_moveitem?' +
            'anchor=%s&delta=%s&item_id=%s')

    def test_show_hide_url(self):
        """Test that show/hide url is correctly compiled."""
        from raptus.article.core.interfaces import IManageable
        article = self.portal.article

        url = IManageable(article).show_hide_url
        self.assertEquals(url,
            'http://nohost/plone/article/@@article_showhideitem?' +
            'anchor=%s&action=%s&uid=%s&component=%s')

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


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
