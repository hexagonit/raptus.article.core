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


class TestGetOrderedViewlets(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.componentfilter.get_ordered_viewlets()."""

    def makeNamelessViewlet(self, name):
        """Creates a mock viewlet withouth a __name__."""
        viewlet = mock.Mock(spec="nothing".split())
        return viewlet

    def makeViewletManager(self, viewlets):
        """Creates a mock viewlet manager."""

        # define a mocked viewlet manager
        class MockedManager(mock.Mock):
            @property
            def viewlets(self):
                return viewlets

        return MockedManager()

    def test_no_viewlet_managers(self):
        """Test retriving an ordered list of viewlets when no viewlet managers
        are specified."""
        from raptus.article.core.componentfilter import ComponentFilter
        from raptus.article.core import componentfilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # override ORDERED_VIEWLET_MANAGERS to be an empty list
        componentfilter.ORDERED_VIEWLET_MANAGERS = []

        # test
        order = filter.get_ordered_viewlets()
        self.assertEquals(len(order), 0)

    @mock.patch('raptus.article.core.componentfilter.ComponentFilter.get_viewlet_manager')
    def test_invalid_manager(self, get_viewlet_manager):
        """Test retriving a list of ordered viewlets when a viewlet manager
        is invalid and cannot be found."""
        from zope.component.interfaces import ComponentLookupError
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # self.get_viewlet_manager(name, iface) throws the ComponentLookupError
        get_viewlet_manager.return_value = None
        get_viewlet_manager.side_effect = ComponentLookupError('foo')

        # test that get_ordered_viewlets does not crash when it receives
        # the ComponentLookupError
        order = filter.get_ordered_viewlets()
        self.assertEquals(len(order), 0)

    @mock.patch(
    'raptus.article.core.componentfilter.ComponentFilter.get_viewlet_manager')
    def test_viewlet_without_name(self, get_viewlet_manager):
        """Test retriving a list of ordered viewlets when a viewlet does not
        have a __name__."""
        from raptus.article.core.componentfilter import ComponentFilter
        from raptus.article.core import componentfilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # override ORDERED_VIEWLET_MANAGERS to only have one item
        componentfilter.ORDERED_VIEWLET_MANAGERS = [('foo', 'bar')]

        # create mocked viewlet and viewlet manager
        viewlet = self.makeNamelessViewlet('mocked.viewlet')
        manager = self.makeViewletManager((viewlet, ))

        # override get_viewlet_manager() to return our mocked manager
        get_viewlet_manager.return_value = manager

        # test that get_ordered_viewlets does not crash when it receives
        # the ComponentLookupError
        order = filter.get_ordered_viewlets()
        self.assertEquals(len(order), 0)


class TestGetOrderdViewletsIntegration(RACoreIntegrationTestCase):
    """Test get_ordered_viewlets() method of
    raptus.article.core.componentfilter."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_get_ordered_viewlets(self):
        """Test retriving a list of viewlets ordered by their viewlet
        managers."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = self.portal.article
        request = self.layer['request']
        view = self.portal.restrictedTraverse('article')
        filter = ComponentFilter(context, request, view)

        # test
        order = filter.get_ordered_viewlets()
        self.assertEquals(len(order), 29)
        self.assertEquals(order[0], u'plone.htmlhead.dublincore')
        self.assertEquals(order[len(order) - 1], u'plone.analytics')


class TestGetViewletManagerIntegration(RACoreIntegrationTestCase):
    """Test get_viewlet_manager() method of
    raptus.article.core.componentfilter."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_retrieve_viewlet_manager(self):
        """Test retriving a viewlet manager."""
        from raptus.article.core.componentfilter import ComponentFilter
        from plone.app.layout.viewlets.interfaces import IHtmlHead

        # prepare instance of ComponentFilter
        context = self.portal.article
        request = self.layer['request']
        view = self.portal.restrictedTraverse('article')
        filter = ComponentFilter(context, request, view)

        # test
        manager = filter.get_viewlet_manager('plone.htmlhead', IHtmlHead)
        self.assertTrue(manager)
        self.assertTrue(IHtmlHead.providedBy(manager))


class TestSortComponents(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.componentfilter.sort_components()."""

    def makeComponent(self, viewlet):
        """Creates a mock component."""
        class MockedComponent(mock.Mock):
            @property
            def viewlet(self):
                return viewlet
        return MockedComponent()

    def test_no_components(self):
        """Test when there are no components."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        # test
        components = filter.sort_components([], [])
        self.assertEquals(0, len(components))

    def test_sort_components(self):
        """Test sorting components."""
        from raptus.article.core.componentfilter import ComponentFilter

        # prepare instance of ComponentFilter
        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view
        filter = ComponentFilter(context, request, view)

        components = [
            ('foo', self.makeComponent('foo')),
            ('bar', self.makeComponent('bar')),
            ('gallery', self.makeComponent('gallery')),
        ]

        order = (
            'bar',
            'gallery',
            'foo',
        )

        # test
        sorted_comps = filter.sort_components(components, order)
        self.assertEquals(3, len(sorted_comps))
        self.assertEquals([comp[0] for comp in sorted_comps],
                          'bar gallery foo'.split())


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
