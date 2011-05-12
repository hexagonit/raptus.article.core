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

    def get_active_components(self):
        """Get components that are activated for Article."""
        from raptus.article.core.interfaces import IComponents
        return IComponents(self.portal.article).activeComponents()

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_activate_component(self):
        """Test that _save() activates components set in request."""
        # check that no components are active by default
        self.assertEquals(0, len(self.get_active_components()))

        # call _save() to activate related component
        self.request.form['form.components'] = u'related'
        view = self.portal.article.restrictedTraverse('@@components')
        result = view._save()
        self.assertEquals(True, result)

        # check that r.a.related component is now active
        active_components = self.get_active_components()
        self.assertEquals(1, len(active_components))
        name, comp = active_components[0]
        self.assertEquals(name, 'related')

    def test_deactivate_component(self):
        """Test that _save() deactivates components set in request."""
        # check that no components are active by default
        self.assertEquals(0, len(self.get_active_components()))

        # activate the default component
        from raptus.article.core.browser.related import IRelated
        alsoProvides(self.portal.article, IRelated)
        self.assertEquals(1, len(self.get_active_components()))

        # call _save() to deactivate related component
        view = self.portal.article.restrictedTraverse('@@components')
        result = view._save()
        self.assertEquals(True, result)

        # check that r.a.related component is deactivated
        active_components = self.get_active_components()
        self.assertEquals(0, len(active_components))

    def test_default_component(self):
        """Test component 'related' that is available by default."""

        # activate the default component
        from raptus.article.core.browser.related import IRelated
        alsoProvides(self.portal.article, IRelated)

        view = self.portal.article.restrictedTraverse('@@components')
        results = view.components
        self.assertEquals(1, len(results))
        self.assertEquals(results[0]['selected'], True)
        self.assertEquals(results[0]['name'], u'related')
        self.assertEquals(results[0]['title'], u'Related content')
        self.assertEquals(results[0]['image'], '++resource++related.gif')
        self.assertEquals(results[0]['description'], u'List of related content of the article.')

    def test_default_output(self):
        """Test default html output of @@components."""

        # activate the default component
        from raptus.article.core.browser.related import IRelated
        alsoProvides(self.portal.article, IRelated)

        # we need to set this so we can get our view's output
        self.request.set('URL', self.portal.article.absolute_url() + '/@@components')
        self.request.set('ACTUAL_URL', self.portal.article.absolute_url() + '/@@components')

        view = self.portal.article.restrictedTraverse('@@components')
        output = view()
        self.assertIn('Component selection', output)
        self.assertIn('Related content', output)
        self.assertIn('List of related content of the article.', output)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
