# -*- coding: utf-8 -*-
"""Tests for Components selected by default."""

import mock
import unittest2 as unittest


class TestSetDefaults(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.componentsdefault.SetDefaults().
    """

    def makeComponent(self, interface):
        """Creates a mock component."""
        component = mock.Mock(spec='interface'.split())
        component.interface.providedBy.return_value = interface
        return component

    def makeProvider(self, components):
        """Make a mock provider."""
        provider = mock.Mock(spec='getComponents'.split())
        provider.getComponents.return_value = components
        return provider

    @mock.patch('raptus.article.core.componentsdefault.component')
    @mock.patch('raptus.article.core.componentsdefault.interface')
    def test_setting_default_interfaces(self, zope_interface, zope_component):
        """Test that default interfaces are being set."""
        from raptus.article.core.componentsdefault import SetDefaults
        from raptus.article.core.interfaces import IDefaultComponents

        # prepare mocked components
        components = [
            self.makeComponent('IFoo'),
            self.makeComponent('IBar'),
            ]

        # prepare mocked providers
        providers = [
            ('foo', self.makeProvider(components)),
            ]

        # prepare zope.event
        event = mock.sentinel.event

        # prepare Article object
        article = mock.Mock(spec="reindexObject".split())

        # patch ZCA
        zope_component.getAdapters.return_value = providers
        zope_interface.alsoProvides.return_value = True

        # test
        SetDefaults(article, event)

        zope_component.getAdapters.assert_called_once_with((article,), IDefaultComponents)

        self.assertEquals(zope_interface.alsoProvides.call_count, 2)
        zope_interface.alsoProvides.assert_called_with(article, components[1].interface)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
