# -*- coding: utf-8 -*-
from Acquisition import aq_parent

from OFS.SimpleItem import SimpleItem

from zope.component import adapts
from zope.event import notify
from zope.interface import Interface
from zope.interface import implements
from zope.lifecycleevent import ObjectAddedEvent
from zope.formlib import form
from plone.contentrules.engine.interfaces import IRuleExecutor

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
from sc.contentrules.groupbydate.events import ObjectGroupedByDate

from sc.contentrules.groupbydate import MessageFactory as _


class GroupByDateAction(SimpleItem):
    """
    """
    implements(IGroupByDateAction, IRuleElementData)

    base_folder = ''
    structure = '%Y/%m/%d'
    container = ('folder', 'Folder')

    element = 'sc.contentrules.actions.groupbydate'

    @property
    def summary(self):
        return _(u"Move the item under ${base_folder} using ${structure} structure",
                 mapping=dict(base_folder=self.base_folder,
                              structure=self.structure))


class GroupByDateActionExecutor(MoveActionExecutor):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, IGroupByDateAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        self.wt = getToolByName(context, 'portal_workflow')

    def __call__(self):
        '''  Executes action, moving content to a date based folder structure
        '''
        context = self.context
        self._pstate = context.unrestrictedTraverse('@@plone_portal_state')
        self._portal = self._pstate.portal()
        self._portalPath = list(self._portal.getPhysicalPath())

        # Get event object
        obj = self.event.object

        # This should get us a DateTime or a datetime (dexterity)
        objDate = obj.effective_date

        base_folder = self.element.base_folder
        structure = self.element.structure

        folder = self._base_folder(str(base_folder), obj)

        if folder is None:
            self.error(obj, _(u"Base folder ${target} does not exist.",
                       mapping={'target': base_folder}))
            return False

        destFolder = self._createFolderStructure(folder,
                                                 structure, date=objDate)
        destFolderRelPath = self._relPathToPortal(destFolder)

        self.element.target_folder = '/'.join(destFolderRelPath)

        # get the future id
        next_id = self.generate_id(destFolder, obj.id)
        # Move object
        result = super(GroupByDateActionExecutor, self).__call__()
        self.element.target_folder = None
        # notify specific event on new object
        new_obj = destFolder[next_id]
        notify(ObjectGroupedByDate(new_obj))
        return result

    def _relPathToPortal(self, obj):
        ''' Given an object we return it's relative path to portal
        '''
        portalPath = self._portalPath
        return list(obj.getPhysicalPath())[len(portalPath):]

    def _base_folder(self, base_folder, obj):
        ''' Given a base_folder string and the object triggering the event, we
            return the base object to be used by this action.
        '''
        # Large portions of this code came from Products.ATContentTypes
        # TODO: a package to deal with this kind of stuff (string to object?)
        # sanitize a bit: you never know, with all those win users out there
        relPath = base_folder.replace("\\", "/")
        if not relPath:
            return self._portal
        if relPath[0] == '/':
            # someone didn't enter a relative path.
            # let's go with it
            path = relPath.split('/')[1:]
        else:
            folders = relPath.split('/')

            # set the path to the object path
            path = self._relPathToPortal(aq_parent(obj))

            # now construct an aboslute path based on the relative custom path
            # eat away from 'path' whenever we encounter a '..'
            # in the relative path apend all other elements other than ..
            for folder in folders:
                if folder == '..':
                    # chop off one level from path
                    if path == []:
                        # can't chop off more
                        # just return this path and leave the loop
                        break
                    else:
                        path = path[:-1]
                elif folder == '.':
                    # don't really need this but for being complete
                    # strictly speaking some user may use a . aswell
                    pass  # do nothing
                else:
                    path.append(folder)

        if not (path == []):
            # As we will traverse from portal, there is no need to
            # have its path in the way
            path = '/'.join(path)
            try:
                baseFolder = self._portal.unrestrictedTraverse(path)
            except (AttributeError, KeyError):
                baseFolder = None
        else:
            baseFolder = self._portal
        return baseFolder

    def _createFolderStructure(self, folder, structure='ymd', date=None):
        ''' Create a folder structure and then return our innermost folder
        '''
        if not date:
            date = DateTime()

        dateFormat = structure

        date = date.strftime(dateFormat)

        folderStructure = [str(p) for p in date.split('/')]

        container = self.element.container
        # We run IRuleExecutor here to make sure other rules will be
        # executed for the newly created folders
        executor = IRuleExecutor(self.context, None)
        for fId in folderStructure:
            if not fId in folder.objectIds():
                _createObjectByType(container, folder, id=fId,
                                    title=fId, description=fId)
                folder = folder[fId]
                event = ObjectAddedEvent(folder, aq_parent(folder), fId)
                if executor is not None:
                    executor(event)
            else:
                folder = folder[fId]
        return folder


class GroupByDateAddForm(AddForm):
    """
    An add form for the group by date action
    """
    form_fields = form.FormFields(IGroupByDateAction)
    label = _(u"Add group by date folder action")
    description = _(u"A content rules action to move an item to a folder"
                    u" structure.")

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
    description = _(u"A content rules action to move an item to a folder"
                    u" structure.")
