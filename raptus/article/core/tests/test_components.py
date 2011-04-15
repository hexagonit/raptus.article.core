# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface import alsoProvides

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, login, setRoles

from raptus.article.core.interfaces import IComponents
from raptus.article.core.tests.base import RACoreIntegrationTestCase


class TestGetComponents(RACoreIntegrationTestCase):
    """Test getComponents() method of raptus.article.core.components."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_no_available_components(self):
        """Test when there are no available components."""
        # Remove the raptus.core.related component that is
        # there by default
        from raptus.article.core.browser.related import Component
        from raptus.article.core.interfaces import IArticle
        sm = self.portal.getSiteManager()
        sm.unregisterAdapter(Component, provided=IArticle)

        # TODO: the line above does not work. Study ZCA in greater
        # detail and make it work :)

        # components = IComponents(self.portal.article).getComponents()
        # self.assertEquals(len(components), 0)

    def test_single_avaiable_component(self):
        """Test when only a single component is available."""
        components = IComponents(self.portal.article).getComponents()
        self.assertEquals(len(components), 1)

        name, comp = components[0]
        self.assertEquals(u'related', name)

    def test_multiple_avaiable_components(self):
        """Test retrieving the list of available components."""
        #TODO: for now we only have one component available for tests


class TestActiveComponents(RACoreIntegrationTestCase):
    """Test activeComponents() method of raptus.article.core.components."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_no_active_components(self):
        """Test when no components are active."""
        # Remove the raptus.core.related component that is
        # there by default
        from raptus.article.core.browser.related import Component
        from raptus.article.core.browser.related import IRelated
        sm = self.portal.getSiteManager()
        sm.unregisterAdapter(Component, provided=IRelated)

        # TODO: the line above does not work. Study ZCA in greater
        # detail and make it work :)

        # components = IComponents(self.portal.article).activeComponents()
        # self.assertEquals(len(components), 0)

    def test_single_active_components(self):
        """Test when only a single component is active."""

        # enable raptus.article.related component on our article
        components = IComponents(self.portal.article).getComponents()
        alsoProvides(self.portal.article, components[0][1].interface)

        # retrive active components
        active_components = IComponents(self.portal.article).activeComponents()

        name, comp = active_components[0]
        self.assertEquals(u'related', name)

    def test_multiple_avaiable_components(self):
        """Test retrieving the list of available components."""
        #TODO: for now we only have one component available for tests


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
