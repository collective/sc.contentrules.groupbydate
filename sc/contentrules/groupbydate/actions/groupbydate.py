
# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface
from zope.interface import implements
from zope.formlib import form

from zope.schema import Int
from zope.schema import getFieldsInOrder

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm

from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.contentrules.rule.interfaces import IRuleElementData
from plone.contentrules.rule.interfaces import IExecutable

from plone.app.contentrules.actions.move import MoveActionExecutor

from DateTime import DateTime

from sc.contentrules.groupbydate.interfaces import IGroupByDateAction
from sc.contentrules.groupbydate import MessageFactory as _

class GroupByDateAction(SimpleItem):
    """
    
    """
    implements(IGroupByDateAction, IRuleElementData)
    
    base_folder = ''
    structure = 'ymd'
    
    element = 'sc.contentrules.actions.groupbydate'
    
    @property
    def summary(self):
        return _(u"Move the item under ${base_folder} using ${structure} structure",
                mapping=dict(field=self.base_folder,structure=self.structure))
    

class GroupByDateActionExecutor(MoveActionExecutor):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IGroupByDateAction, Interface)
    
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
    
    def __call__(self):
        # Get event object
        obj = self.event.object
        objDate = obj.getEffectiveDate() or obj.created()
        # We must remove the first /
        base_folder = self.element.base_folder[1:]
        structure = self.element.structure
        portal = getToolByName(self.context,'portal_url').getPortalObject()
        
        folder = portal.unrestrictedTraverse(str(base_folder), None)
        
        if folder is None:
            self.error(obj, _(u"Base folder ${target} does not exist.", mapping={'target' : base_folder}))
            return False
        destination_folder = self._createFolderStructure(folder,structure,date=objDate)
        self.element.target_folder = '%s/%s' % (base_folder,destination_folder)
        
        # Move object
        result = super(GroupByDateActionExecutor,self).__call__()
        self.element.target_folder = None
        return result
        
    
    def _createFolderStructure(self,folder,structure='ymd',date=None):
        '''
        '''
        wt = getToolByName(self.context,'portal_workflow')
        if not date:
            date = DateTime()
        if structure == 'ymd':
            dateFormat = '%Y/%m/%d'
        elif structure == 'ym':
            dateFormat = '%Y/%m'
        elif structure == 'y':
            dateFormat = '%Y'
        else:
            return ''
        folderStructure = [str(p) for p in date.strftime(dateFormat).split('/')]
        for fId in folderStructure:
            if not fId in folder.objectIds():
                _createObjectByType('Folder', folder, id=fId,
                                    title=fId, description=fId)
            folder = folder[fId]
            # XXX: Need to define a transition for this folder
            #wt.doActionFor(folder,'publish')
        
        return date.strftime(dateFormat)


class GroupByDateAddForm(AddForm):
    """
    An add form for the group by date action
    """
    form_fields = form.FormFields(IGroupByDateAction)
    label = _(u"Add group by date folder action")
    description = _(u"A content rules action to move an item to a folder structure.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = GroupByDateAction()
        form.applyChanges(a, self.form_fields, data)
        return a

class GroupByDateEditForm(EditForm):
    """
    An edit form for the group by date action
    """
    form_fields = form.FormFields(IGroupByDateAction)
    form_fields['base_folder'].custom_widget = UberSelectionWidget
    label = _(u"Edit group by date action")
    description = _(u"A content rules action to move an item to a folder structure.")
    form_name = _(u"Configure element")


    