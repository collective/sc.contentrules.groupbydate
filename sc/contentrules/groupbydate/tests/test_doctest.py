import unittest2 as unittest
import doctest

from plone.testing import layered

from sc.contentrules.groupbydate.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/validator.txt',
                                     package='sc.contentrules.groupbydate'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite