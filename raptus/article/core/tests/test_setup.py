# -*- coding: utf-8 -*-

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from raptus.article.core.tests.base import RACoreIntegrationTestCase


class TestInstall(RACoreIntegrationTestCase):
    """Test installation of raptus.article.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    # cssregistry.xml
    def test_css_registered(self):
        """Test if CSS files are registered with portal_css."""
        resources = self.portal.portal_css.getResources()

        ids = [r.getId() for r in resources]

        self.assertTrue('raptus.article.css' in ids,
                        'raptus.article.css not found in portal_css')

    # types.xml
    # factorytool.xml
    def test_article_installed(self):
        """Test if Raptus Article is in the list of Portal Types."""

        # test that Article is present in portal_types
        types = getToolByName(self.portal, 'portal_types')
        self.failUnless('Article' in types.objectIds())

        # test that Article is present in portal_factory
        factory = getToolByName(self.portal, 'portal_factory')
        self.failUnless('Article' in factory.getFactoryTypes().keys())

    # Document.xml
    def test_document_disabled(self):
        """Test that Document is not allowed to be added."""
        types = getToolByName(self.portal, 'portal_types')
        document_fti = getattr(types, 'Document')
        self.failIf(document_fti.global_allow)

    # skins.xml
    def test_skins_folders_registered(self):
        """Test if all ./skins folders are registered."""
        skins = getToolByName(self.portal, 'portal_skins')
        skin_layer = skins.getSkinPath('Plone Default')

        self.assertTrue('raptus_article_core' in skin_layer,
                    'raptus_article_core skin folder is not registered')

    # rolemap.xml
    def test_permission_mappings(self):
        """Test correct assigning of permissions."""

        # Test permission mapping for adding an Article
        self.assertEquals(
            self.portal._raptus_article__Add_Article_Permission,
            ('Manager', 'Contributor', 'Owner')
            )

        # Test permission mapping for managing Components
        self.assertEquals(
            self.portal._raptus_article__Manage_Components_Permission,
            ('Manager', 'Editor', 'Owner')
            )

    # propertiestool.xml
    def test_site_properties(self):
        """Test if site properties are correctly set."""

        site_props = self.portal.portal_properties.site_properties

        # Article must be among default Page types
        self.assertEquals(site_props.default_page_types, ('Topic', 'Article'))


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
