# -*- coding: utf-8 -*-
"""Tests for showing/hiding Items in Articles."""

import mock
import unittest2 as unittest

from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from zope.publisher.browser import TestRequest

from raptus.article.core.tests.base import RACoreIntegrationTestCase


class TestCall(unittest.TestCase):
    """Unit tests for edge cases of __call__() of ShowHideItem of
    r.a.core.browser.showhide.
    """

    def makeShowHideItem(self, form={}):
        """Prepares an instance of ShowHideItem."""
        from raptus.article.core.browser.showhide import ShowHideItem
        context = mock.Mock(spec=''.split())
        request = TestRequest(form=form)
        return ShowHideItem(context, request)

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    def test_queryAdapter_none(self, redirect):
        """Test that ShowHideItem() returns None when no Component is found
        for context.
        """
        redirect.return_value = True

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide(None, None, 'foo'))  # action, uid, component

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    def test_no_item(self, get_item, queryAdapter, redirect):
        """Test that ShowHideItem() returns None when no item of this UID
        is found.
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value = False

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide(None, 'foo', None))  # action, uid, component

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_components')
    def test_no_components(self, get_components, get_item, queryAdapter, redirect):
        """Test that ShowHideItem() returns None when no item of this UID
        is found.
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value = True
        get_components.return_value = []

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide(None, None, 'foo'))  # action, uid, component

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_components')
    def test_get_components_raises(self, get_components, get_item, queryAdapter, redirect):
        """Test that ShowHideItem() does not crash if there is an error with retrieving
        components with get_components().
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value = True
        get_components.return_value = []
        get_components.side_effect = Exception()

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide(None, None, 'foo'))  # action, uid, component

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_components')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.set_item_show')
    def test_item_show(self, set_item_show, get_components, get_item, queryAdapter, redirect):
        """Test that item is shown in this component by this component being added
        to the 'components' field of item.
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value.reindexObject.return_value = True
        get_components.return_value = []
        set_item_show.return_value = True

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide('show', None, 'foo'))  # action, uid, component
        get_item.return_value.reindexObject.assert_called_once()

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_components')
    def test_item_show_already_shown(self, get_components, get_item, queryAdapter, redirect):
        """Test that nothing happens if user wants to show an item that is
        already shown -> component is already in items' 'components' field.
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value.reindexObject.return_value = True
        get_components.return_value = ['foo']

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide('show', None, 'foo'))  # action, uid, component

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_components')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.set_item_hide')
    def test_item_hide(self, set_item_hide, get_components, get_item, queryAdapter, redirect):
        """Test that item is hidden in this component by this component being added
        to the 'components' field of item.
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value.reindexObject.return_value = True
        get_components.return_value = ['foo']
        set_item_hide.return_value = True

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide('hide', None, 'foo'))  # action, uid, component
        get_item.return_value.reindexObject.assert_called_once()

    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.redirect')
    @mock.patch('raptus.article.core.browser.showhide.queryAdapter')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_item')
    @mock.patch('raptus.article.core.browser.showhide.ShowHideItem.get_components')
    def test_item_hide_already_hidden(self, get_components, get_item, queryAdapter, redirect):
        """Test that nothing happens if user wants to hide an item that is
        already hidden -> component is not in items' 'components' field.
        """
        redirect.return_value = True
        queryAdapter.return_value = True
        get_item.return_value.reindexObject.return_value = True
        get_components.return_value = []

        showhide = self.makeShowHideItem()
        self.assertEquals(None, showhide('hide', None, 'foo'))  # action, uid, component


class TestShowHideViewIntegration(RACoreIntegrationTestCase):
    """Integration tests for @@article_showhide BrowserView."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_get_item(self):
        """Test that get_item() returns a correct object."""
        article = self.portal.article
        view = article.restrictedTraverse('@@article_showhideitem')
        self.assertEquals(article, view.get_item(article.UID()))

    def test_get_item_none(self):
        """Test that get_item() returns None if it cannot
        find an item with this UID."""
        article = self.portal.article
        view = article.restrictedTraverse('@@article_showhideitem')
        self.assertEquals(None, view.get_item('foo'))

    def test_redirect(self):
        """Test that user gets redirected to a correct url and anchor."""
        # mock RESPONSE so we can trace what redirect() was called with
        self.layer['request'].RESPONSE = mock.Mock(spec='redirect'.split())

        # do redirect
        view = self.portal.article.restrictedTraverse('@@article_showhideitem')
        view.redirect('foo')

        # test
        self.layer['request'].RESPONSE.redirect.assert_called_with('http://nohost/plone/article#foo')

    def test_default_output(self):
        """Test default output of @@article_showhide."""
        view = self.portal.article.restrictedTraverse('@@article_showhideitem')
        output = view(None, None, None)
        self.assertEquals(None, output)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
