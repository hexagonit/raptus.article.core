# -*- coding: utf-8 -*-
"""Tests for the 'raptus.related' component that comes bundled with this
package by default.
"""

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import mock
import unittest2 as unittest


class TestRelated(RACoreIntegrationTestCase):
    """Unit tests for related() of Viewlet of r.a.core.browser.related."""

    def makeViewlet(self, related_objects):
        """Prepares an instance of Viewlet."""
        from raptus.article.core.browser.related import Viewlet

        # context returns a list of related objects
        context = mock.Mock(spec='computeRelatedItems'.split())
        context.computeRelatedItems.return_value = related_objects

        request = mock.Mock(spec=''.split())
        return Viewlet(context, request, None)

    def makeRelatedObject(self, obj_id='article', portal_type='Article'):
        """Prepares an object that can be related."""
        obj = mock.Mock(spec="portal_type getId Title Description absolute_url".split())
        obj.portal_type = portal_type
        obj.getId.return_value = obj_id
        obj.Title.return_value = portal_type
        obj.Description.return_value = "%s's description" % portal_type
        obj.absolute_url.return_value = 'http://nohost/plone/%s' % obj_id
        return obj

    @mock.patch('raptus.article.core.browser.related.component')
    @mock.patch('raptus.article.core.browser.related.Viewlet.get_types_that_use_view_action')
    def test_related_item(self, get_types_that_use_view_action, zope_component,):
        """Test attributes of returned related item."""
        # patch get_types_that_use_view_action()
        get_types_that_use_view_action.return_value = []

        # patch zope.component
        zope_component.getMultiAdapter.return_value.getIcon.return_value.url = 'http://nohost/plone/icon'

        # prepare return values of context.computeRelatedItems
        related_objects = [self.makeRelatedObject(), ]

        # get an instance of the Viewlet
        viewlet = self.makeViewlet(related_objects)

        self.assertEquals(1, len(viewlet.related))

        item = viewlet.related[0]
        self.assertEquals(item['id'], 'article')
        self.assertEquals(item['title'], 'Article')
        self.assertEquals(item['description'], "Article's description")
        self.assertEquals(item['url'], 'http://nohost/plone/article')
        self.assertEquals(item['icon'], 'http://nohost/plone/icon')

    @mock.patch('raptus.article.core.browser.related.component')
    @mock.patch('raptus.article.core.browser.related.Viewlet.get_types_that_use_view_action')
    def test_use_view_action(self, get_types_that_use_view_action, zope_component,):
        """Test url for content-types that need '/view' appended to their
        absolute urls.
        """
        # patch get_types_that_use_view_action()
        get_types_that_use_view_action.return_value = ['Image']

        # prepare return values of context.computeRelatedItems
        related_objects = [self.makeRelatedObject(obj_id='image', portal_type='Image'), ]

        # get an instance of the Viewlet
        viewlet = self.makeViewlet(related_objects)

        self.assertEquals(1, len(viewlet.related))

        item = viewlet.related[0]
        self.assertEquals(item['id'], 'image')
        self.assertEquals(item['title'], 'Image')
        self.assertEquals(item['url'], 'http://nohost/plone/image/view')  # test that url ends with '/view'


class TestRelatedIntegration(RACoreIntegrationTestCase):
    """Test classes and viewlets of r.a.core.browser.related."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_component(self):
        """Test default attributes of Component."""

        from raptus.article.core.browser.related import IRelated
        from raptus.article.core.browser.related import Component
        component = Component(self.portal.article)

        self.assertEquals(component.title, 'Related content')
        self.assertEquals(component.description, 'List of related content of the article.')
        self.assertEquals(component.image, '++resource++related.gif')
        self.assertEquals(component.interface, IRelated)
        self.assertEquals(component.viewlet, 'raptus.article.related')
        self.assertEquals(component.context, self.portal.article)

    def test_viewlet(self):
        """Test Viewlet."""
        from raptus.article.core.browser.related import Viewlet
        viewlet = Viewlet(self.portal.article, self.layer['request'], None)
        related = viewlet.related
        self.assertEquals(0, len(related))

    def test_default_viewlet_returns_nothing(self):
        """Test that Plone's default RelatedItemsViewlet returns
        an empty string.
        """
        from raptus.article.core.browser.related import RelatedItemsViewlet
        viewlet = RelatedItemsViewlet(self.portal.article, self.layer['request'], None)
        self.assertEquals('', viewlet.index())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
