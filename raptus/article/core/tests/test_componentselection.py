# -*- coding: utf-8 -*-
"""Tests for ComponentSelection Archetypes vocabulary and widget."""

from Products.CMFPlone.FactoryTool import TempFolder
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase

import mock
import unittest2 as unittest


class TestComponentSelectionVocabulary(unittest.TestCase):
    """Unit-tests for edge-cases of __call__() of
    ComponentSelectionVocabulary.
    """

    def makeComponentSelectionVocabulary(self):
        """Prepares an instance of ComponentFilter."""
        from raptus.article.core.componentselection import ComponentSelectionVocabulary
        return ComponentSelectionVocabulary()

    def makeComponent(self, title):
        """Prepares an instance of a dummy Component."""
        component = mock.Mock(spec='title'.split())
        component.title = title
        return component

    @mock.patch('raptus.article.core.componentselection.ComponentSelectionVocabulary.get_containing_article')
    def test_no_container(self, get_containing_article):
        """Test return value when there is a problem getting item's container."""
        vocabulary = self.makeComponentSelectionVocabulary()

        get_containing_article.return_value = False
        context = mock.sentinel.mock

        items = vocabulary(context)
        self.assertEquals([], items)

    @mock.patch('raptus.article.core.componentselection.component')
    @mock.patch('raptus.article.core.componentselection.ComponentSelectionVocabulary.get_selectable_components')
    @mock.patch('raptus.article.core.componentselection.ComponentSelectionVocabulary.get_containing_article')
    def test_no_components(self, get_containing_article, get_selectable_components, zope_component):
        """Test return value when there are no components."""
        vocabulary = self.makeComponentSelectionVocabulary()

        get_containing_article.return_value = mock.sentinel.container
        zope_component.getMultiAdapter.return_value = mock.Mock(spec='filter'.split())
        zope_component.getMultiAdapter.return_value.filter.return_value = []
        context = mock.Mock(spec='REQUEST'.split())

        items = vocabulary(context)
        self.assertEquals([], items)

    @mock.patch('raptus.article.core.componentselection.component')
    @mock.patch('raptus.article.core.componentselection.ComponentSelectionVocabulary.get_selectable_components')
    @mock.patch('raptus.article.core.componentselection.ComponentSelectionVocabulary.get_containing_article')
    def test_multiple_components(self, get_containing_article, get_selectable_components, zope_component):
        """Test return value when there are multiple components."""
        vocabulary = self.makeComponentSelectionVocabulary()

        context = mock.Mock(spec='REQUEST'.split())
        get_containing_article.return_value = mock.sentinel.container
        zope_component.getMultiAdapter.return_value.filter.return_value = [
            ('foo', self.makeComponent('Foo')),
            ('bar', self.makeComponent('Bar')),
        ]

        items = vocabulary(context)
        self.assertEquals('Foo Bar'.split(), [i.title for i in items])


class TestGetContainingArticle(unittest.TestCase):
    """Unit-tests for edge-cases of get_containing_article()"""

    def makeComponentSelectionVocabulary(self):
        """Prepares an instance of ComponentFilter."""
        from raptus.article.core.componentselection import ComponentSelectionVocabulary
        return ComponentSelectionVocabulary()

    @mock.patch('raptus.article.core.componentselection.aq_parent')
    @mock.patch('raptus.article.core.componentselection.IArticle')
    def test_item_in_creation(self, IArticle, aq_parent):
        """Test that get_containing_article() returns a 3 level higher parent,
        if the Item is just being created.
        """

        IArticle.providedBy.return_value = True
        aq_parent.return_value = mock.Mock(spec=TempFolder)

        context = mock.Mock(spec='isTemporary'.split())
        context.isTemporary.return_value = True

        vocabulary = self.makeComponentSelectionVocabulary()
        container = vocabulary.get_containing_article(context)

        self.assertIsInstance(container, mock.Mock)
        self.assertEquals(3, aq_parent.call_count)

    @mock.patch('raptus.article.core.componentselection.aq_parent')
    @mock.patch('raptus.article.core.componentselection.IArticle')
    def test_container_is_article(self, IArticle, aq_parent):
        """Test that get_containing_article() returns a direct parent,
        if that parent is an Article.
        """

        IArticle.providedBy.return_value = True

        context = mock.Mock(spec='isTemporary'.split())
        context.isTemporary.return_value = False

        vocabulary = self.makeComponentSelectionVocabulary()
        container = vocabulary.get_containing_article(context)

        self.assertIsInstance(container, mock.Mock)
        self.assertEquals(1, aq_parent.call_count)

    @mock.patch('raptus.article.core.componentselection.IArticle')
    def test_container_not_article(self, IArticle):
        """Test that get_containing_article() returns False,
        if the container is not an Article.
        """

        IArticle.providedBy.return_value = False

        context = mock.Mock(spec='isTemporary'.split())
        context.isTemporary.return_value = False

        vocabulary = self.makeComponentSelectionVocabulary()
        container = vocabulary.get_containing_article(context)

        self.assertEquals(container, False)


class TestGetSelectableComponents(unittest.TestCase):
    """Unit tests for logic of all edge cases in
    get_selectable_components().
    """

    def makeComponentSelectionVocabulary(self):
        """Prepares an instance of ComponentFilter."""
        from raptus.article.core.componentselection import ComponentSelectionVocabulary
        return ComponentSelectionVocabulary()

    @mock.patch('raptus.article.core.componentselection.component')
    def test_no_available_components(self, zope_component):
        """Test when there are no available components."""
        from raptus.article.core.interfaces import IComponentSelection

        zope_component.getAdapters.return_value = []

        context = mock.sentinel.context

        vocabulary = self.makeComponentSelectionVocabulary()
        components = vocabulary.get_selectable_components(context)
        self.assertEquals(0, len(components))
        zope_component.getAdapters.assert_called_once_with((context, ), IComponentSelection)

    @mock.patch('raptus.article.core.componentselection.component')
    def test_multiple_available_components(self, zope_component):
        """Test when multiple available components are available."""
        from raptus.article.core.interfaces import IComponentSelection

        context = mock.sentinel.context
        zope_component.getAdapters.return_value = [
            ('foo', 'raptus.article.core.browser.foo.Component'),
            ('bar', 'raptus.article.core.browser.bar.Component'),
        ]

        vocabulary = self.makeComponentSelectionVocabulary()
        components = vocabulary.get_selectable_components(context)
        self.assertEquals(components, [
            ('foo', 'raptus.article.core.browser.foo.Component'),
            ('bar', 'raptus.article.core.browser.bar.Component'),
        ])
        zope_component.getAdapters.assert_called_once_with((context, ), IComponentSelection)


class TestComponentSelectionWidgetIntegration(RACoreIntegrationTestCase):
    """Integration tests for ComponentSelectionWidget."""

    def makeComponentSelectionWidget(self):
        """Prepares an instance of ComponentSelectionWidget."""
        from raptus.article.core.componentselection import ComponentSelectionWidget
        return ComponentSelectionWidget()

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_is_visible(self):
        """Test is_visible() of ComponentSelectionWidget on a child
        of Article.
        """

        # create a subcontent in Article
        self.portal.article.invokeFactory('Folder', 'subfolder')
        subfolder = self.portal.article.subfolder

        # check if subfolder is contained in an Article
        widget = self.makeComponentSelectionWidget()
        self.assertEquals('visible', widget.isVisible(subfolder))

    def test_not_visible(self):
        """Test is_visible() of ComponentSelectionWidget on a non-Article
        child.
        """
        widget = self.makeComponentSelectionWidget()
        self.assertEquals('invisible', widget.isVisible(self.portal))


class TestComponentSelectionDefaultIntegration(RACoreIntegrationTestCase):
    """Integration tests for ComponentSelectionDefault."""

    def makeComponentSelectionDefault(self):
        """Prepares an instance of ComponentSelectionDefault."""
        from raptus.article.core.componentselection import ComponentSelectionDefault
        return ComponentSelectionDefault(self.portal.article)

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_call(self):
        """Test __call__() of ComponentSelectionWidget."""
        default = self.makeComponentSelectionDefault()
        self.assertEquals([], default())


class TestComponentSelectionVocabularyIntegration(RACoreIntegrationTestCase):
    """Integration tests for ComponentSelectionVocabulary."""

    def makeComponentSelectionVocabulary(self):
        """Prepares an instance of ComponentSelectionVocabulary."""
        from raptus.article.core.componentselection import ComponentSelectionVocabulary
        return ComponentSelectionVocabulary()

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

    def test_call(self):
        """Test __call__() of ComponentSelectionVocabulary."""
        vocabulary = self.makeComponentSelectionVocabulary()
        self.assertEquals([], vocabulary(self.portal.article))


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
