# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import mock
import unittest2 as unittest


class TestFilterComponents(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    raptus.article.core.components.componentfilter.filter()."""

    def test_no_components(self):
        """Test when there are components."""
        from raptus.article.core.componentfilter import ComponentFilter

        context = mock.sentinel.context
        request = mock.sentinel.request
        view = mock.sentinel.view

        sorter = ComponentFilter(context, request, view)
        components = sorter.filter([])
        self.assertEquals(0, len(components))


class TestFilterComponentsIntegration(RACoreIntegrationTestCase):
    """Test filter() method of raptus.article.core.componentfilter."""

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
        sorter = ComponentFilter(context, request, view)

        # get a list of RA components to pass into filtering
        components = IComponents(self.portal.article).getComponents()
        self.assertEquals(len(components), 1)

        # test
        sorted_components = sorter.filter(components)
        self.assertEquals(len(sorted_components), 1)

        name, comp = sorted_components[0]
        self.assertEquals(u'related', name)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
