# -*- coding: utf-8 -*-
"""Tests for installation and setup of this package."""

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from raptus.article.core.tests.base import RACoreIntegrationTestCase
from zope.component import queryMultiAdapter
from zope.viewlet.interfaces import IViewletManager

import unittest2 as unittest


class TestInstall(RACoreIntegrationTestCase):
    """Test installation of raptus.article.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if raptus.article.core is installed with
        portal_quickinstaller.
        """

        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('raptus.article.core'))

    # import_steps.xml
    def test_custom_setuphandlers(self):
        """Test if custom install code in setuphandlers.py."""
        catalog = getToolByName(self.portal, 'portal_catalog')
        self.assertTrue('component' in catalog.indexes())

    # cssregistry.xml
    def test_css_registered(self):
        """Test if CSS files are registered with portal_css."""
        resources = self.portal.portal_css.getResources()

        ids = [r.getId() for r in resources]

        self.assertTrue('raptus.article.css' in ids,
                        'raptus.article.css not found in portal_css')

    # types.xml
    # factorytool.xml
    # tinymce.xml
    def test_article_installed(self):
        """Test if Raptus Article is in the list of Portal Types."""

        # test that Article is added to portal_types
        types = getToolByName(self.portal, 'portal_types')
        self.failUnless('Article' in types.objectIds())

        # test that Article is added to portal_factory
        factory = getToolByName(self.portal, 'portal_factory')
        self.failUnless('Article' in factory.getFactoryTypes().keys())

        # test that Article is added to TinyMCE
        tinymce = getToolByName(self.portal, 'portal_tinymce')
        self.failUnless('Article' in tinymce.linkable)
        self.failUnless('Article' in tinymce.containsobjects)
        self.failUnless('Article' in tinymce.containsanchors)

    # Document.xml
    def test_document_disabled(self):
        """Test that Document is not allowed to be added."""
        types = getToolByName(self.portal, 'portal_types')
        document_fti = getattr(types, 'Document')
        self.failIf(document_fti.global_allow)

    # skins.xml
    def test_skins_folder_registered(self):
        """Test if raptus_article_core skins folders is registered."""
        skins = getToolByName(self.portal, 'portal_skins')
        skin_layer = skins.getSkinPath('Plone Default')

        self.assertTrue('raptus_article_core' in skin_layer,
                        'raptus_article_core skin folder is not registered')

    # rolemap.xml
    def test_permission_mappings(self):
        """Test correct assigning of permissions."""

        # Test permission mapping for adding an Article
        self.assertEquals(('Manager', 'Contributor', 'Owner'),
                          self.portal._raptus_article__Add_Article_Permission)

        # Test permission mapping for managing Components
        self.assertEquals(('Manager', 'Editor', 'Owner'),
                          self.portal._raptus_article__Manage_Components_Permission)

    # propertiestool.xml
    def test_site_properties(self):
        """Test if site properties are correctly set."""

        site_props = self.portal.portal_properties.site_properties

        # Article must be among default Page types
        self.assertEquals(site_props.default_page_types, ('Topic', 'Article'))

    # viewlets.xml
    def test_related_viewlet_registered(self):
        """Test if raptus.article.related viewlet is registered for
        plone.belowcontentbody viewlet manager.
        """

        # add test Article
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.portal.invokeFactory('Article', 'article')

        # we need a context and request
        context = self.portal.article
        request = self.layer['request']

        # viewlet managers also require a view object for adaptation
        view = BrowserView(context, request)

        # finally, you need the name of the manager you want to find
        manager_name = 'plone.belowcontentbody'

        # viewlet managers are found by Multi-Adapter lookup
        manager = queryMultiAdapter((context, request, view), IViewletManager, manager_name, default=None)
        self.failUnless(manager)

        # calling update() on a manager causes it to set up its viewlets
        manager.update()

        # get viewlet names
        viewlets = [v.__name__ for v in manager.viewlets]

        # is our viewlet present?
        self.assertTrue("plone.belowcontentbody.relateditems" in viewlets)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
