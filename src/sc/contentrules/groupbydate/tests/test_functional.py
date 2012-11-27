# -*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from sc.contentrules.groupbydate.testing import FUNCTIONAL_TESTING

optionflags = doctest.REPORT_ONLY_FIRST_FAILURE


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('controlpanel.txt',
                                     optionflags=optionflags),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
