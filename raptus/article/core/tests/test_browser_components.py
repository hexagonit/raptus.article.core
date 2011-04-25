# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase
from zope.interface import alsoProvides

import unittest2 as unittest


class TestComponentsIntegration(RACoreIntegrationTestCase):
    """Test components() method of raptus.article.core.browser.components."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_default_component(self):
        """Test component 'related' that is available by default."""
        from raptus.article.core.browser.related import IRelated

        # activate the default component
        alsoProvides(self.portal.article, IRelated)

        view = self.portal.article.restrictedTraverse('@@components')
        results = view.components
        self.assertEquals(1, len(results))
        self.assertEquals(results[0]['selected'], True)
        self.assertEquals(results[0]['name'], u'related')
        self.assertEquals(results[0]['title'], u'Related content')
        self.assertEquals(results[0]['image'], '++resource++related.gif')
        self.assertEquals(results[0]['description'],
                          u'List of related content of the article.')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
