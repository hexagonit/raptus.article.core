# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, login, setRoles

from raptus.article.core.interfaces import IComponents
from raptus.article.core.tests.base import RACoreIntegrationTestCase


class TestView(RACoreIntegrationTestCase):
    """Test @@components BrowserView."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    # def test_component_filter(self):
    #     """Test filtering and sorting of components
    #     based on the registrations of their viewlets.
    #     """
        #TODO

    def test_get_components(self):
        """Test retrieving the list of available components."""
        components = IComponents(self.portal.article).getComponents()
        self.assertEquals(u'related', components[0][0])

    def test_active_components(self):
        """Test retrieving the list of active components."""

        # enable raptus.article.related component on our article
        components = IComponents(self.portal.article).getComponents()
        alsoProvides(self.portal.article, components[0][1].interface)

        # retrive active components
        components = IComponents(self.portal.article).activeComponents()
        self.assertEquals(u'related', components[0][0])


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
