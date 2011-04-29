# -*- coding: utf-8 -*-

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from raptus.article.core.tests.base import RACoreIntegrationTestCase


class TestInstall(RACoreIntegrationTestCase):
    """Test installation of raptus.article.core into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_css_registered(self):
        """Test if CSS files are registered with portal_css."""
        resources = self.portal.portal_css.getResources()

        ids = [r.getId() for r in resources]

        self.assertTrue('raptus.article.css' in ids,
                        'raptus.article.css not found in portal_css')

    def test_skins_folders_registered(self):
        """Test if all ./skins folders are registered."""
        skins = getToolByName(self.portal, 'portal_skins')
        skin_layer = skins.getSkinPath('Plone Default')

        self.assertTrue('raptus_article_core' in skin_layer,
                    'raptus_article_core skin folder is not registered')

    def test_rolemap(self):
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

    def test_site_properties(self):
        """Test if site properties are correcty set."""

        site_props = self.portal.portal_properties.site_properties

        # Meta-keywords must be enabled
        self.assertEquals(site_props.default_page_types, ('Topic', 'Article'))


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
