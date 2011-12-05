# -*- coding: utf-8 -*-

from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import sc.contentrules.groupbydate
        self.loadZCML(package=sc.contentrules.groupbydate)
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'sc.contentrules.groupbydate:default')
        wf = getattr(portal, 'portal_workflow')
        types = ('Document', 'Folder', 'Link', 'Topic')
        wf.setChainForPortalTypes(types, 'simple_publication_workflow')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.contentrules.groupbydate:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='sc.contentrules.groupbydate:Functional',
    )
