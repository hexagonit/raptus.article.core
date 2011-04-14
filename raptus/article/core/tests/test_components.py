# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID

from raptus.article.core.tests.base import RACoreFunctionalTestCase


class TestView(RACoreFunctionalTestCase):
    """Test @@components BrowserView."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_component_filter(self):
        """Test filtering and sorting of components based on the registrations
        of their viewlets.
        """
        #TODO

    def test_get_components(self):
        """Test retrieving the list of available components.
        """
        #TODO

    def test_active_components(self):
        """Test retrieving the list of active components.
        """
        #TODO

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
