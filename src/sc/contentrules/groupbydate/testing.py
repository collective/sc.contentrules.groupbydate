# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import sc.contentrules.groupbydate
        self.loadZCML(package=sc.contentrules.groupbydate)


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE, ),
    name='sc.contentrules.groupbydate:Integration',
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, ),
    name='sc.contentrules.groupbydate:Functional',
)
