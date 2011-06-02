# -*- coding: utf-8 -*-
"""Tests for ZCML definition of a Component."""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase
from zope.configuration import xmlconfig
from zope.interface import Interface

import mock
import unittest2 as unittest


class TestSelection(unittest.TestCase):
    """Test edge cases of selection argument."""

    @mock.patch('raptus.article.core.zcml.adapter')
    @mock.patch('raptus.article.core.zcml.viewletDirective')
    def test_no_selection(self, viewlet_directive, zope_adapter):
        """Test that IArticle is used as for= parameter for adapter() call,
        if selection is is not set.
        """

        zope_adapter.return_value = True
        viewlet_directive.return_value = True

        context = mock.Mock()
        name = 'foo'
        component = mock.Mock()
        viewlet = mock.Mock()
        manager = mock.Mock()

        from raptus.article.core.zcml import registerComponent
        registerComponent(context, name, component, viewlet, manager)

        self.assertTrue(zope_adapter.called)
        self.assertEquals(zope_adapter.call_count, 1)

        from raptus.article.core.interfaces import IComponent
        from raptus.article.core.interfaces import IArticle
        args = (context, [component], IComponent)
        kwargs = {'name': name, 'for_': [IArticle]}
        self.assertEquals(zope_adapter.call_args, (args, kwargs))

    @mock.patch('raptus.article.core.zcml.adapter')
    @mock.patch('raptus.article.core.zcml.viewletDirective')
    def test_selection(self, viewlet_directive, zope_adapter):
        """Test that selection is used as for= parameter for adapter() call,
        when selection is set.
        """
        class IFoo(Interface):
            pass

        zope_adapter.return_value = True
        viewlet_directive.return_value = True

        context = mock.Mock()
        name = 'foo'
        component = mock.Mock()
        viewlet = mock.Mock()
        manager = mock.Mock()

        from raptus.article.core.zcml import registerComponent
        registerComponent(context, name, component, viewlet, manager, selection=IFoo)

        self.assertTrue(zope_adapter.called)
        self.assertEquals(zope_adapter.call_count, 2)

        from raptus.article.core.interfaces import IComponentSelection
        args = (context, [component], IComponentSelection)
        kwargs = {'name': name, 'for_': [IFoo]}
        self.assertEquals(zope_adapter.call_args, (args, kwargs))


class TestImage(unittest.TestCase):
    """Test edge cases of setting component's image."""

    @mock.patch('raptus.article.core.zcml.adapter')
    @mock.patch('raptus.article.core.zcml.viewletDirective')
    @mock.patch('raptus.article.core.zcml.resource')
    def test_no_image(self, resource, viewlet_directive, zope_adapter):
        """Test that image is not set if it's not passed and it cannot
        be retrieved from context.path.
        """

        zope_adapter.return_value = True
        viewlet_directive.return_value = True

        context = mock.Mock()
        name = 'foo'
        component = mock.Mock()
        viewlet = mock.Mock()
        manager = mock.Mock()

        from raptus.article.core.zcml import registerComponent
        registerComponent(context, name, component, viewlet, manager)

        self.assertFalse(resource.called)

    @mock.patch('raptus.article.core.zcml.adapter')
    @mock.patch('raptus.article.core.zcml.viewletDirective')
    @mock.patch('raptus.article.core.zcml.resource')
    def test_image(self, resource, viewlet_directive, zope_adapter):
        """Test that image is set."""

        zope_adapter.return_value = True
        viewlet_directive.return_value = True

        context = mock.Mock()
        name = 'foo'
        component = mock.Mock()
        viewlet = mock.Mock()
        manager = mock.Mock()
        image = 'bar'

        from raptus.article.core.zcml import registerComponent
        registerComponent(context, name, component, viewlet, manager, image=image)

        self.assertTrue(resource.called)
        self.assertEquals(resource.call_count, 1)

        args = (context, component.image.replace('++resource++', ''))
        kwargs = {'image': image}
        self.assertEquals(resource.call_args, (args, kwargs))

    @mock.patch('raptus.article.core.zcml.adapter')
    @mock.patch('raptus.article.core.zcml.viewletDirective')
    @mock.patch('raptus.article.core.zcml.resource')
    @mock.patch('raptus.article.core.zcml.os')
    def test_image_from_path(self, os, resource, viewlet_directive, zope_adapter):
        """Test that image is retrived from path if it's not passed."""

        zope_adapter.return_value = True
        viewlet_directive.return_value = True
        os.path.abspath.return_value = 'bar'
        os.path.isfile.return_value = True

        context = mock.Mock()
        name = 'foo'
        component = mock.Mock()
        viewlet = mock.Mock()
        manager = mock.Mock()

        from raptus.article.core.zcml import registerComponent
        registerComponent(context, name, component, viewlet, manager)

        self.assertTrue(resource.called)
        self.assertEquals(resource.call_count, 1)

        args = (context, component.image.replace('++resource++', ''))
        kwargs = {'image': 'bar'}
        self.assertEquals(resource.call_args, (args, kwargs))


class TestIntegration(RACoreIntegrationTestCase):
    """Test registering a new Raptus Article Component."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_register_component(self):
        """Test registering a new Raptus Article Component."""
        import raptus.article.core
        context = xmlconfig.file('meta.zcml', raptus.article.core)
        xmlconfig.file('tests/foo.zcml', raptus.article.core, context=context)

        from raptus.article.core.interfaces import IComponents
        components = IComponents(self.portal.article).getComponents()
        self.assertEquals(2, len(components))
        name, comp = components[0]
        self.assertEquals('foo.bar', name)
        self.assertEquals(u'Föö', comp.title)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
