# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID

from raptus.article.core.tests.base import RACoreFunctionalTestCase


class TestView(RACoreFunctionalTestCase):
    """Test @@components BrowserView."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        
        # add initial test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Article', 'article')
    
def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
