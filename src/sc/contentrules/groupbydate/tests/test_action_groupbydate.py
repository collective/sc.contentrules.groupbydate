# -*- coding:utf-8 -*-

import unittest2 as unittest

from DateTime import DateTime

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from zope.interface import implements
from zope.component import getUtility, getMultiAdapter
from zope.component.interfaces import IObjectEvent

from plone.app.contentrules.rule import Rule

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IExecutable

from Products.CMFDefault.Document import Document

from Products.ATContentTypes.content.topic import ATTopic

from sc.contentrules.groupbydate.actions.groupbydate import GroupByDateAction
from sc.contentrules.groupbydate.actions.groupbydate import GroupByDateEditForm

from sc.contentrules.groupbydate.testing import INTEGRATION_TESTING


class DummyEvent(object):
    implements(IObjectEvent)

    def __init__(self, object):
        self.object = object


class TestGroupByDateAction(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'target')
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal['folder']
        self.folder.invokeFactory('Document', 'd1')
        self.folder.d1.setEffectiveDate(DateTime('2009/04/22'))
        self.folder.invokeFactory('Folder', 'relativeTarget')
        o = Document('cmf', 'CMF Content', '', '', '')
        o.setEffectiveDate(DateTime('2009/04/22'))
        self.folder._setObject('cmf', o, suppress_events=True)

    def testRegistered(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.groupbydate')
        self.assertEquals('sc.contentrules.actions.groupbydate',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)

    def testInvokeAddView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.groupbydate')
        storage = getUtility(IRuleStorage)
        storage[u'foo'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.portal.REQUEST),
                                 name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.createAndAdd(data={'base_folder': '/target',
                                   'structure': 'ymd'})

        e = rule.actions[0]
        self.failUnless(isinstance(e, GroupByDateAction))
        self.assertEquals('/target', e.base_folder)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.groupbydate')
        e = GroupByDateAction()
        editview = getMultiAdapter((e, self.folder.REQUEST),
                                   name=element.editview)
        self.failUnless(isinstance(editview, GroupByDateEditForm))

    def testActionSummary(self):
        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'
        e.roles = set(['Reader', ])
        summary = (u"Move the item under ${base_folder} using ${structure} "
                   u"structure")
        self.assertEquals(summary, e.summary)

    def testExecute(self):
        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('%s/2009/04/22' %
                                                         e.base_folder[1:])
        self.failUnless('d1' in target_folder.objectIds())

    def testExecuteWithError(self):
        e = GroupByDateAction()
        e.base_folder = '/dummy'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(False, ex())

        self.failUnless('d1' in self.folder.objectIds())
        self.failIf('d1' in self.portal.target.objectIds())

    def testExecuteWithoutPermissionsOnTarget(self):
        setRoles(self.portal, TEST_USER_ID, ['Member', ])

        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('%s/2009/04/22' %
                                                         e.base_folder[1:])
        self.failUnless('d1' in target_folder.objectIds())

    def testExecuteWithNamingConflict(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        target_folder_path = '2009/04/22'.split('/')

        target_folder = self.portal.target
        for folder in target_folder_path:
            if not folder in target_folder.objectIds():
                target_folder.invokeFactory('Folder', folder)
            target_folder = target_folder[folder]
        target_folder.invokeFactory('Document', 'd1')

        setRoles(self.portal, TEST_USER_ID, ['Member', ])

        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        self.failUnless('d1' in target_folder.objectIds())
        self.failUnless('d1.1' in target_folder.objectIds())

    def testExecuteWithSameSourceAndTargetFolder(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', ])
        target_folder_path = '2009/04/22'.split('/')

        target_folder = self.portal.target
        for folder in target_folder_path:
            if not folder in target_folder.objectIds():
                target_folder.invokeFactory('Folder', folder)
            target_folder = target_folder[folder]

        target_folder.invokeFactory('Document', 'd1')
        target_folder.d1.setEffectiveDate(DateTime('2009/04/22'))

        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'

        ex = getMultiAdapter((target_folder, e, DummyEvent(target_folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.assertEquals(['d1'], list(target_folder.objectIds()))

    def testExecuteWithRelativePath(self):
        ''' Execute the action with a valid relative path
        '''
        e = GroupByDateAction()
        # A sibling folder named relativeTarget
        e.base_folder = './relativeTarget'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        relativeTarget = self.folder.relativeTarget
        target_folder = relativeTarget.unrestrictedTraverse('2009/04/22')
        self.failUnless('d1' in target_folder.objectIds())

    def testExecuteWithLongRelativePath(self):
        ''' Execute the action with a valid relative path
        '''
        folder = self.folder['relativeTarget']
        folder.invokeFactory('Document', 'd2')
        folder.d2.setEffectiveDate(DateTime('2009/04/22'))
        e = GroupByDateAction()
        # A sibling folder named relativeTarget
        e.base_folder = '../../'
        e.container = 'Folder'

        ex = getMultiAdapter((folder, e, DummyEvent(folder.d2)), IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d2' in folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('2009/04/22')
        self.failUnless('d2' in target_folder.objectIds())

    def testExecuteWithoutBaseFolder(self):
        ''' Execute the action without a path
        '''
        e = GroupByDateAction()
        # A sibling folder named relativeTarget
        e.base_folder = ''
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('2009/04/22')
        self.failUnless('d1' in target_folder.objectIds())

    def testExecuteWithoutEffectiveDate(self):
        ''' Execute the action without an effective date
        '''
        folder = self.folder['relativeTarget']
        folder.invokeFactory('Document', 'd2')
        e = GroupByDateAction()
        # A sibling folder named relativeTarget
        e.base_folder = '../'
        e.container = 'Folder'

        ex = getMultiAdapter((folder, e, DummyEvent(folder.d2)), IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d2' in folder.objectIds())
        path = DateTime().strftime('%Y/%m/%d')
        target_folder = self.folder.unrestrictedTraverse(path)
        self.failUnless('d2' in target_folder.objectIds())

    def testExecuteWithNonExistantRelativePath(self):
        ''' Execute the action with a non existent relative path
        '''
        e = GroupByDateAction()
        # An non existant folder
        e.base_folder = '../relativeTarget'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(False, ex())

        self.failUnless('d1' in self.folder.objectIds())

    def testExecuteFromPloneSite(self):
        ''' Execute the action with a non existent relative path
        '''
        e = GroupByDateAction()
        self.portal.invokeFactory('Document', 'd2')
        self.portal.d2.setEffectiveDate(DateTime('2009/04/22'))
        # An non existant folder
        e.base_folder = '..'
        e.container = 'Folder'

        ex = getMultiAdapter((self.portal, e, DummyEvent(self.portal.d2)),
                             IExecutable)
        self.assertEquals(True, ex())

        target_folder = self.portal.unrestrictedTraverse('2009/04/22')
        self.failUnless('d2' in target_folder.objectIds())

    def testExecuteDifferentContainer(self):
        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Topic'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('%s/2009/04/22' %
                                                         e.base_folder[1:])
        self.assertTrue(isinstance(target_folder, ATTopic))

    def testStrftimeFmt(self):
        ''' Execute the action using a valid strftime formatting string
        '''
        e = GroupByDateAction()
        e.base_folder = '/target'
        e.structure = '%Y/%m'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('%s/2009/04' %
                                                         e.base_folder[1:])
        self.failUnless('d1' in target_folder.objectIds())

    def testWrongStrftimeFmt(self):
        ''' Execute the action using a typoed strftime formatting string
        '''
        e = GroupByDateAction()
        e.base_folder = '/target'
        e.structure = 'Y/%m'
        e.container = 'Folder'

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('d1' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('%s/Y/04' %
                                                         e.base_folder[1:])
        self.failUnless('d1' in target_folder.objectIds())

    def testExecutionOnCMFContent(self):
        ''' Tests if the rules works with CMF Content
        '''
        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'

        o = self.folder['cmf']

        ex = getMultiAdapter((self.folder, e, DummyEvent(o)),
                             IExecutable)
        self.assertEquals(True, ex())

        self.failIf('cmf' in self.folder.objectIds())
        target_folder = self.portal.unrestrictedTraverse('%s/2009/04/22' %
                                                         e.base_folder[1:])
        self.failUnless('cmf' in target_folder.objectIds())

    def testFolderNotifyAddedEvent(self):
        from zope.component import adapter
        from zope.component import provideHandler
        from zope.lifecycleevent import ObjectAddedEvent

        e = GroupByDateAction()
        e.base_folder = '/target'
        e.container = 'Folder'

        class Handler(object):

            def __init__(self):
                self.invocations = []
                self.counter = 0

            @adapter(ObjectAddedEvent)
            def handler(self, event):
                obj = event.object
                self.counter += 1
                if not obj in self.invocations:
                    self.invocations.append(obj)

        self.handler = Handler()
        provideHandler(self.handler.handler)

        ex = getMultiAdapter((self.folder, e, DummyEvent(self.folder.d1)),
                             IExecutable)
        self.assertEquals(True, ex())
        invocations = self.handler.invocations
        self.assertEquals(len(invocations), 3)
        self.assertEquals(self.handler.counter, 3)
        self.assertEquals(invocations[0].getId(), '2009')
        self.assertEquals(invocations[1].getId(), '04')
        self.assertEquals(invocations[2].getId(), '22')
