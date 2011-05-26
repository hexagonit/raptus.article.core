# -*- coding: utf-8 -*-
"""Tests for utility methods for retrieving avaiable and active Components. """

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import unittest2 as unittest


class TestGetIntegration(RACoreIntegrationTestCase):
    """Test get() method of raptus.article.core.componentsconfiguration."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def makeComponentsConfiguration(self):
        """Make an instance of ComponentsConfiguration."""
        from raptus.article.core.interfaces import IComponentsConfiguration
        return IComponentsConfiguration(self.portal.article)

    def test_configuration_key_not_found_return_none(self):
        """Returns None, if configuration key is not found."""
        configuration = self.makeComponentsConfiguration()
        self.assertEquals(configuration.get('foo'), None)

    def test_configuration_key_not_found_return_default(self):
        """Returns a default value passed in as a second argument,
        if configuration key is not found."""
        configuration = self.makeComponentsConfiguration()
        self.assertEquals(configuration.get('foo', 'bar'), 'bar')

    def test_return_configuration_value(self):
        """Returns the configuration key's value."""
        self.portal.portal_properties.raptus_article._setProperty('foo', 'bar')
        configuration = self.makeComponentsConfiguration()
        self.assertEquals(configuration.get('foo'), 'bar')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
