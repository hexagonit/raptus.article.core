# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from raptus.article.core.tests.base import RACoreIntegrationTestCase

import unittest2 as unittest


class TestComponentSelectionWidgetIntegration(RACoreIntegrationTestCase):
    """Integration tests for ComponentSelectionWidget."""

    def makeComponentSelectionWidget(self):
        """Prepares an instance of ComponentSelectionWidget."""
        from raptus.article.core.componentselection import ComponentSelectionWidget
        return ComponentSelectionWidget()

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_is_visible(self):
        """Test is_visible() of ComponentSelectionWidget on a child
        of Article."""

        # create a subcontent in Article
        self.portal.article.invokeFactory('Folder', 'subfolder')
        subfolder = self.portal.article.subfolder

        # check if subfolder is contained in an Article
        widget = self.makeComponentSelectionWidget()
        self.assertEquals('visible', widget.isVisible(subfolder))

    def test_not_visible(self):
        """Test is_visible() of ComponentSelectionWidget on a non-Article
        child.
        """
        widget = self.makeComponentSelectionWidget()
        self.assertEquals('invisible', widget.isVisible(self.portal))


class TestComponentSelectionDefaultIntegration(RACoreIntegrationTestCase):
    """Integration tests for ComponentSelectionDefault."""

    def makeComponentSelectionDefault(self):
        """Prepares an instance of ComponentSelectionDefault."""
        from raptus.article.core.componentselection import ComponentSelectionDefault
        return ComponentSelectionDefault(self.portal.article)

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_call(self):
        """Test __call__() of ComponentSelectionWidget."""
        default = self.makeComponentSelectionDefault()
        self.assertEquals([], default())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
