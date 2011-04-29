# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import mock
import unittest2 as unittest


class TestProvideAllInterfaces(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.componentfilter.provide_all_interfaces()."""

    def makeComponent(self, provided, iface):
        """Creates a mock component that is either provided or not."""
        comp = mock.Mock(spec='interface'.split())
        comp.interface.providedBy.return_value = provided
        comp.interface.iface.return_value = iface
        return comp

    def test_no_components(self):
        """Test when there are no components."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # test
        components = filter.provide_all_interfaces([])
        self.assertEquals(0, len(components))

    def test_all_interfaces_provided(self):
        """Test when all components' interfaces are already provided."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # prepare dummy components
        components = [
            ('foo', self.makeComponent(provided=True, iface='foo')),
            ('bar', self.makeComponent(provided=True, iface='bar')),
            ]

        # test
        components = filter.provide_all_interfaces(components)
        self.assertEquals(0, len(components))

    @mock.patch('raptus.article.core.componentfilter.interface')
    def test_no_interfaces_provided(self, zope_interface):
        """Test when none of components' interfaces are already provided."""
        from raptus.article.core.componentfilter import ComponentFilter

        zope_interface.alsoProvides.return_value = True

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # prepare dummy components
        components = [
            ('foo', self.makeComponent(provided=False, iface='foo')),
            ('bar', self.makeComponent(provided=False, iface='bar')),
            ]

        # test
        interfaces = filter.provide_all_interfaces(components)
        self.assertEquals(2, len(interfaces))
        self.assertEquals([i.iface() for i in interfaces], 'foo bar'.split())

    @mock.patch('raptus.article.core.componentfilter.interface')
    def test_some_interfaces_provided(self, zope_interface):
        """Test when some of components' interfaces are already provided."""
        from raptus.article.core.componentfilter import ComponentFilter

        zope_interface.alsoProvides.return_value = True

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # prepare dummy components
        components = [
            ('foo', self.makeComponent(provided=False, iface='foo')),
            ('bar', self.makeComponent(provided=True, iface='bar')),
            ('gallery', self.makeComponent(provided=False, iface='gallery')),
            ]

        # test
        interfaces = filter.provide_all_interfaces(components)
        self.assertEquals(2, len(interfaces))
        self.assertEquals([i.iface() for i in interfaces],
                          'foo gallery'.split())


class TestUnprovideNotprovided(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.componentfilter.unprovide_notprovided()."""

    def makeInterface(self):
        """Creates a mock interface."""
        comp = mock.Mock(spec='interface'.split())
        comp.interface.noLongerProvides.return_value = True
        return comp

    def test_no_interfaces(self):
        """Test when there are no interfaces in notprovided list."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # test
        filter.unprovide_notprovided([])

    @mock.patch('raptus.article.core.componentfilter.interface')
    def test_unprovide_interfaces(self, zope_interface):
        """Test unproviding interfaces notprovided list."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        zope_interface.noLongerProvides.return_value = True

        # test
        filter.unprovide_notprovided("foo bar".split())
        self.assertEquals(zope_interface.noLongerProvides.call_count, 2)


class TestFilter(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.componentfilter.filter()."""

    def test_no_components(self):
        """Test when there are no components."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # test
        components = filter.filter([])
        self.assertEquals(0, len(components))


class TestFilterIntegration(RACoreIntegrationTestCase):
    """Test filter() method of raptus.article.core.componentfilter"""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_default_component(self):
        """Test sorting components available by default."""
        from raptus.article.core.componentfilter import ComponentFilter
        from raptus.article.core.interfaces import IComponents

        # prepare instance of ComponentFilter
        context = self.portal.article
        request = self.layer['request']
        view = self.portal.restrictedTraverse('article')
        filter = ComponentFilter(context, request, view)

        # get a list of RA components to pass into filtering
        components = IComponents(self.portal.article).getComponents()
        self.assertEquals(len(components), 1)

        # test
        sorted_components = filter.filter(components)
        self.assertEquals(len(sorted_components), 1)

        name, comp = sorted_components[0]
        self.assertEquals(u'related', name)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
