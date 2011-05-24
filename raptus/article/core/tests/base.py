# -*- coding: utf-8 -*-
"""Layers and TestCases for our tests."""

from __future__ import with_statement

import unittest2 as unittest

from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE


class RaptusArticleCoreLayer(PloneSandboxLayer):
    """Layer for Raptus Article Core tests."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import raptus.article.core
        self.loadZCML(package=raptus.article.core)
        self.loadZCML('overrides.zcml', package=raptus.article.core)
        z2.installProduct(app, 'raptus.article.core')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'raptus.article.core:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'raptus.article.core')


# FIXTURES
RAPTUS_ARTICLE_CORE_FIXTURE = RaptusArticleCoreLayer()

# LAYERS
INTEGRATION_TESTING = IntegrationTesting(
    bases=(RAPTUS_ARTICLE_CORE_FIXTURE, ),
    name="raptus.article.core:Integration")

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RAPTUS_ARTICLE_CORE_FIXTURE,),
    name="raptus.article.core:Functional")


# TESTCASES
class RACoreIntegrationTestCase(unittest.TestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = INTEGRATION_TESTING


class RACoreFunctionalTestCase(unittest.TestCase):
    """We use this base class for all functional tests in this package -
    tests that require a full-blown Plone instance for testing.
    """
    layer = FUNCTIONAL_TESTING
