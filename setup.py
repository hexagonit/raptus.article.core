from setuptools import setup, find_packages
import os

version = '2.0b8'

install_requires = [
    'manuel',
    'mock',
    'plone.app.testing',
    'setuptools',
    'unittest2',
    ]

setup(name='raptus.article.core',
      version=version,
      description="Provides a configurable article content type (replaces the default Page content type).",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "MANUAL.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Raptus AG',
      author_email='dev@raptus.com',
      url='http://raptus.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['raptus', 'raptus.article'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
