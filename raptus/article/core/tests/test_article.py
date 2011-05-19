# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_NAME, TEST_USER_ID, login, setRoles

from raptus.article.core.tests.base import RACoreIntegrationTestCase


class TestArticleViewIntegration(RACoreIntegrationTestCase):
    """Integration tests for @@view of Article."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # add initial test content
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article', title='Raptus Article')

    def test_default_output(self):
        """Test default output of @@view."""
        # we need to set this so we can get our view's output
        self.request.set('URL', self.portal.article.absolute_url() + '/@@view')
        self.request.set('ACTUAL_URL', self.portal.article.absolute_url() + '/@@view')

        view = self.portal.article.restrictedTraverse('@@view')
        output = view()
        self.assertTrue('Raptus Article' in output)
        self.assertTrue('class="template-view portaltype-article' in output)


class TestInstall(RACoreIntegrationTestCase):
    """Test installation of raptus.article.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_article_fields(self):
        """Tests if Article's field values are correctly
        stored and can be retrieved."""

        # add test Article
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article',
                             title="Article Title",
                             description="Article Description",
                             text="<b>Article</b> Text",
                             hideTitle=True,
                             hideDescription=True,
                             )

        # test it's fields
        article = self.portal.article
        self.assertEquals(article.title, "Article Title")
        self.assertEquals(article.description, "Article Description")
        self.assertEquals(article.text, "<b>Article</b> Text")
        self.assertEquals(article.hideTitle, True)
        self.assertEquals(article.hideDescription, True)

    def test_display_dropdown_disabled(self):
        """Tests if display drop-down menu is disabled for Articles."""

        # add test Article
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

        # disable display dropdown by overriding canSetDefaultPage
        # so it always returns False
        self.assertEquals(self.portal.article.canSetDefaultPage(), False)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
