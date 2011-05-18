from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login

import mock
import unittest2 as unittest


class TestShowHideViewIntegration(RACoreIntegrationTestCase):
    """Integration tests for @@article_showhide BrowserView."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_get_item(self):
        """Test that get_item() returns a correct object."""
        article = self.portal.article
        view = article.restrictedTraverse('@@article_showhideitem')
        self.assertEquals(article, view.get_item(article.UID()))

    def test_get_item_none(self):
        """Test that get_item() returns None if it cannot
        find an item with this UID."""
        article = self.portal.article
        view = article.restrictedTraverse('@@article_showhideitem')
        self.assertEquals(None, view.get_item('foo'))

    def test_redirect(self):
        """Test that user gets redirected to a correct url and anchor."""
        # mock RESPONSE so we can trace what redirect() was called with
        self.layer['request'].RESPONSE = mock.Mock(spec='redirect'.split())

        # do redirect
        view = self.portal.article.restrictedTraverse('@@article_showhideitem')
        view.redirect('foo')

        # test
        self.layer['request'].RESPONSE.redirect.assert_called_with('http://nohost/plone/article#foo')

    def test_default_output(self):
        """Test default output of @@article_showhide."""
        view = self.portal.article.restrictedTraverse('@@article_showhideitem')
        output = view(None, None, None)
        self.assertEquals(None, output)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
