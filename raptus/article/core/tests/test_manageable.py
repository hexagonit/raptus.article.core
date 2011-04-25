# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import unittest2 as unittest


class TestGetComponentsIntegration(RACoreIntegrationTestCase):
    """TODO"""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_delete_permission(self):
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
