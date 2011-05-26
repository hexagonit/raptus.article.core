# -*- coding: utf-8 -*-
"""Tests for custom install steps in setuphandlers.py."""

import mock
import unittest2 as unittest

from raptus.article.core.setuphandlers import install


class TestInstall(unittest.TestCase):
    """Test edge cases of selection argument."""

    def test_no_readDataFile(self):
        """Test that nothing is done if no 'raptus.article.core_install.txt'
        file is found.
        """
        context = mock.Mock(spec='readDataFile'.split())
        context.readDataFile.return_value = None
        self.assertEquals(None, install(context))

    @mock.patch('raptus.article.core.setuphandlers.getToolByName')
    def test_index_already_installed(self, tool):
        """Test that nothing is done if 'components' index is already
        installed in portal_catalog.
        """
        tool.return_value.indexes.return_value = ['component', ]

        context = mock.Mock(spec='readDataFile getSite'.split())
        context.readDataFile.return_value = True

        install(context)
        self.assertEquals(0, tool.return_value.addIndex.call_count)

    @mock.patch('raptus.article.core.setuphandlers.getToolByName')
    def test_install_dependency(self, tool):
        """Test that a dependency product is installed.
        """
        tool.return_value.indexes.return_value = ['component', ]
        tool.return_value.isProductInstallable.return_value = True
        tool.return_value.isProductInstalled.return_value = False

        context = mock.Mock(spec='readDataFile getSite'.split())
        context.readDataFile.return_value = True

        install(context)
        tool.return_value.installProduct.assert_called_once_with('DynamicHeader')

    @mock.patch('raptus.article.core.setuphandlers.getToolByName')
    def test_reinstall_dependency(self, tool):
        """Test that a dependency product is reinstalled in case the product
        was already installed.
        """
        tool.return_value.indexes.return_value = ['component', ]
        tool.return_value.isProductInstallable.return_value = True
        tool.return_value.isProductInstalled.return_value = True

        context = mock.Mock(spec='readDataFile getSite'.split())
        context.readDataFile.return_value = True

        install(context)
        tool.return_value.reinstallProducts.assert_called_once_with('DynamicHeader')

    @mock.patch('raptus.article.core.setuphandlers.getToolByName')
    def test_dependency_not_installable(self, tool):
        """Test that nothing happens if a dependency product is not
        installable.
        """
        tool.return_value.indexes.return_value = ['component', ]
        tool.return_value.isProductInstallable.return_value = False

        context = mock.Mock(spec='readDataFile getSite'.split())
        context.readDataFile.return_value = True

        install(context)
        self.assertEquals(0, tool.return_value.installProduct.call_count)
        self.assertEquals(0, tool.return_value.reinstallProducts.call_count)


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above.
    """
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
