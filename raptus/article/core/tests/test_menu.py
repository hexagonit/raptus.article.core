from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import unittest2 as unittest


class TestGetMenuItemsIntegration(RACoreIntegrationTestCase):
    """Test getMenuItems() method of r.a.core.browser.menu."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def makeFactoriesMenu(self, context):
        """Prepares an instance of FactoriesMenu."""
        from raptus.article.core.browser.menu import FactoriesMenu
        return FactoriesMenu(context)

    @unittest.expectedFailure
    def test_default_output(self):
        """Test default output of getMenuItems."""

        context = self.portal.article
        request = self.layer['request']
        request.set('URL', self.portal.article.absolute_url() + '/folder_contents')

        menu = self.makeFactoriesMenu(context)

        results = menu.getMenuItems(context, request)
        self.assertEquals(len(results), 3)

        # TODO: this tests fails because the menu object is an instance of
        # Products.Five.metaclass.SimpleViewClass from
        # ./eggs/plone.app.content-2.0.5-py2.6.egg/plone/app/content/browser/folderfactories.pt
        #
        # Instead, it should be an instance of
        # Products.Five.metaclass.SimpleViewClass from
        # ./src/raptus.article.core/raptus/article/core/browser/folderfactories.pt
        # (it's like this when you use bin/instance fg)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
