# -*- coding: utf-8 -*-
"""Tests for utility methods for retrieving available and active Components. """

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase
from zope.interface import alsoProvides

import mock
import unittest2 as unittest


class TestGetComponents(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.Components.getComponents().
    """

    @mock.patch('raptus.article.core.components.component')
    def test_no_available_components(self, zope_component):
        """Test when there are no available components."""
        from raptus.article.core.components import Components
        from raptus.article.core.interfaces import IComponent

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = []

        components = Components(context).getComponents()
        self.assertEquals(0, len(components))
        zope_component.getAdapters.assert_called_once_with((context, ), IComponent)

    @mock.patch('raptus.article.core.components.component')
    def test_multiple_available_components(self, zope_component):
        """Test when multiple available components are available."""
        from raptus.article.core.components import Components
        from raptus.article.core.interfaces import IComponent

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = [
            ('foo', 'raptus.article.core.browser.foo.Component'),
            ('bar', 'raptus.article.core.browser.bar.Component'),
        ]

        components = Components(context).getComponents()
        self.assertEquals(components, [
            ('foo', 'raptus.article.core.browser.foo.Component'),
            ('bar', 'raptus.article.core.browser.bar.Component'),
        ])
        zope_component.getAdapters.assert_called_once_with((context, ), IComponent)


class TestGetComponentsIntegration(RACoreIntegrationTestCase):
    """Test getComponents() method of raptus.article.core.components."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_default_components(self):
        """Test components available by default."""
        from raptus.article.core.interfaces import IComponents
        components = IComponents(self.portal.article).getComponents()
        self.assertEquals(len(components), 1)

        name, comp = components[0]
        self.assertEquals(u'related', name)


class TestActiveComponents(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.Components.activeComponents().
    """

    def makeComponent(self, active):
        """Creates a mock component that is either active or passive."""
        comp = mock.Mock(spec='interface'.split())
        comp.interface.providedBy.return_value = active
        return comp

    @mock.patch('raptus.article.core.components.component')
    def test_no_components(self, zope_component):
        """Test when there are no components registered."""
        from raptus.article.core.components import Components

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = []

        components = Components(context)
        self.assertEquals(len(components.getComponents()), 0)
        self.assertEquals(len(components.activeComponents()), 0)

    @mock.patch('raptus.article.core.components.component')
    def test_no_active_components(self, zope_component):
        """Test when there are components but none are active."""
        from raptus.article.core.components import Components

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = [
            ('foo', self.makeComponent(active=False)),
            ('bar', self.makeComponent(active=False)),
        ]

        components = Components(context)
        self.assertEquals(len(components.getComponents()), 2)
        self.assertEquals(len(components.activeComponents()), 0)

    @mock.patch('raptus.article.core.components.component')
    def test_mixed_components(self, zope_component):
        """Test when there are both active and inactive components."""
        from raptus.article.core.components import Components

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = [
            ('foo', self.makeComponent(active=False)),
            ('bar', self.makeComponent(active=True)),
            ('gallery', self.makeComponent(active=False)),
        ]

        components = Components(context)
        self.assertEquals(len(components.getComponents()), 3)
        self.assertEquals(len(components.activeComponents()), 1)
        name, comp = components.activeComponents()[0]
        self.assertEquals(name, 'bar')

    @mock.patch('raptus.article.core.components.component')
    def test_all_active_components(self, zope_component):
        """Test when all available components are active."""
        from raptus.article.core.components import Components

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = [
            ('foo', self.makeComponent(active=True)),
            ('bar', self.makeComponent(active=True)),
            ('gallery', self.makeComponent(active=True)),
        ]

        components = Components(context)
        self.assertEquals(len(components.getComponents()), 3)
        self.assertEquals(len(components.activeComponents()), 3)

        active_components = [comp[0] for comp in components.activeComponents()]
        self.assertEquals(active_components, 'foo bar gallery'.split())


class TestActiveComponentsIntegration(RACoreIntegrationTestCase):
    """Test activeComponents() method of raptus.article.core.components."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_default_active_components(self):
        """Test when default component is active."""
        from raptus.article.core.interfaces import IComponents

        # enable raptus.article.related component on our article
        components = IComponents(self.portal.article).getComponents()
        alsoProvides(self.portal.article, components[0][1].interface)

        # retrive active components
        active_components = IComponents(self.portal.article).activeComponents()

        name, comp = active_components[0]
        self.assertEquals(u'related', name)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
