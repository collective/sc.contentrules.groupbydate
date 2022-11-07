# -*- coding:utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.0.2.dev0'
description = u"A Plone content rules action that creates a chronological archive."
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='sc.contentrules.groupbydate',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
           "Environment :: Web Environment",
           "Framework :: Plone",
           "Framework :: Plone :: 5.2",
           "Intended Audience :: System Administrators",
           "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
           "Operating System :: OS Independent",
           "Programming Language :: Python",
           "Programming Language :: Python :: 3.8",
           "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone contentrules actions date grouping',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br/',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc', 'sc.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.formlib',
      ],
      extras_require={
          'develop': [
              'Sphinx',
              'manuel',
              'pep8',
              'setuptools-flakes',
          ],
          'test': [
              'interlude',
              'plone.app.testing'
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
