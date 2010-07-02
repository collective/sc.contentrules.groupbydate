# -*- coding: utf-8 -*-
from zope import component
import logging
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup import interfaces as gsinterfaces
from Products.GenericSetup.upgrade import listUpgradeSteps

def upgrade0to1(context):
    ''' Upgrade to version 1.0
    '''
    setup = getToolByName(context, 'portal_setup')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    qi = getToolByName(context,'portal_quickinstaller')
    
    # Install dependencies for this upgrade
    dependencies = [
                    ('Products.CMFPlacefulWorkflow',0,0,'Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow'),
                   ]
    
    for name,locked,hidden,profile in dependencies:
        qi.installProduct(name, locked=locked, hidden=hidden, profile=profile)

    