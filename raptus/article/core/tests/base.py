# -*- coding: utf-8 -*-

import os

import unittest2 as unittest

from zope.configuration import xmlconfig

from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import TEST_USER_NAME, TEST_USER_PASSWORD


class RACoreIntegrationLayer(PloneSandboxLayer):
    """Layer for Raptus Article Core Integration tests."""

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import raptus.article.core
        xmlconfig.file('configure.zcml',
                       raptus.article.core, context=configurationContext)
        z2.installProduct(app, 'raptus.article.core')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'raptus.article.core:default')


class RACoreFunctionalLayer(PloneSandboxLayer):
    """Layer for Raptus Article Core Functional tests."""

    def setUpPloneSite(self, portal):

        # this lets us see all error messages in the error_log.
        portal.error_log._ignored_exceptions = ()

        # show errors in console by monkey patching site error_log service
        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising


# FIXTURES
R_A_CORE_INTEGRATION_FIXTURE = RACoreIntegrationLayer()
R_A_CORE_FUNCTIONAL_FIXTURE = RACoreFunctionalLayer()

# LAYERS
R_A_CORE_INTEGRATION_TESTING = IntegrationTesting(
                            bases=(R_A_CORE_INTEGRATION_FIXTURE, ),
                            name="RACore:Integration")

R_A_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
                            bases=(R_A_CORE_INTEGRATION_FIXTURE,
                                   R_A_CORE_FUNCTIONAL_FIXTURE),
                            name="RACore:Functional")


# TESTCASES
class RACoreIntegrationTestCase(unittest.TestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
    layer = R_A_CORE_INTEGRATION_TESTING


class RACoreFunctionalTestCase(RACoreIntegrationTestCase):
    """We use this base class for all functional tests in this package -
    tests that require a full-blown Plone instance for testing.
    """
    layer = R_A_CORE_FUNCTIONAL_TESTING

    def login_with_browser(self, browser, portal, user=None, password=None):
        """Login to site with testbrowser."""

        if not user:
            user = TEST_USER_NAME
        if not password:
            password = TEST_USER_PASSWORD

        # open site
        browser.open(portal.absolute_url() + '/login')

        # login using the login portlet
        browser.getControl(name='__ac_name').value = user
        browser.getControl(name='__ac_password').value = password
        browser.getControl(name='submit').click()

        # did we get the logged-in message?
        self.failUnless("You are now logged in" in browser.contents)

    def start_zserver(self):
        """Start ZServer so we can inspect site state with a normal browser
        like FireFox."""
        from Testing.ZopeTestCase.utils import startZServer
        echo = startZServer()
        os.system('open http://%s:%s/plone' % echo)

    def open_html(self, browser):
        """Dumps self.browser.contents (HTML) to a file and opens it with
        a normal browser."""
        file = open('/tmp/raptus.article.core.testbrowser.html', 'w')
        file.write(browser.contents)
        os.system('open /tmp/raptus.article.core.testbrowser.html')
