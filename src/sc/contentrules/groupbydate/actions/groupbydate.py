# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from DateTime import DateTime
from OFS.SimpleItem import SimpleItem

from plone.app.contentrules.actions.move import MoveActionExecutor
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.contentrules.engine.interfaces import IRuleExecutor
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData

#from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from sc.contentrules.groupbydate import MessageFactory as _
from sc.contentrules.groupbydate.events import ObjectGroupedByDate
from sc.contentrules.groupbydate.interfaces import IGroupByDateAction

from zope.component import adapter
from zope.event import notify

from zope.interface import implementer
from zope.interface import Interface
from zope.lifecycleevent import ObjectAddedEvent
from plone.app.uuid.utils import uuidToObject


@implementer(IGroupByDateAction, IRuleElementData)
class GroupByDateAction(SimpleItem):
    """
    """

    base_folder = ''                    # uuid
    structure = '%Y/%m/%d'
    container = ('folder', 'Folder')

    element = 'sc.contentrules.actions.groupbydate'

    @property
    def summary(self):
        return _("Move the item under ${base_folder} using ${structure} structure",
                 mapping=dict(base_folder=self.base_folder,
                              structure=self.structure))



@adapter(Interface, IGroupByDateAction, Interface)
@implementer(IExecutable)
class GroupByDateActionExecutor(MoveActionExecutor):
    """ The executor for this action.
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        #self.wt = getToolByName(context, 'portal_workflow')

    def __call__(self):
        """  Executes action, moving content to a date based folder structure
        """
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
        # the target folder could be the same
        next_id = obj.id
        if destFolder != aq_parent(obj):
            next_id = self.generate_id(destFolder, obj.id)
        # Move object
        result = super(GroupByDateActionExecutor, self).__call__()
        self.element.target_folder = None
        # notify specific event on new object
        new_obj = destFolder[next_id]
        notify(ObjectGroupedByDate(new_obj))
        return result

    def _relPathToPortal(self, obj):
        """ Given an object we return it's relative path to portal
        """
        portalPath = self._portalPath
        return list(obj.getPhysicalPath())[len(portalPath):]

    def _base_folder(self, base_folder, obj):
        """ Given a base_folder string and the object triggering the event, we
            return the base object to be used by this action.
        """
        # Large portions of this code came from Products.ATContentTypes
        # TODO: a package to deal with this kind of stuff (string to object?)
        # sanitize a bit: you never know, with all those win users out there
        return uuidToObject(base_folder)

    def _createFolderStructure(self, folder, structure='ymd', date=None):
        """ Create a folder structure and then return our innermost folder
        """
        if not date:
            date = DateTime()

        dateFormat = structure

        date = date.strftime(dateFormat)

        folderStructure = [str(p) for p in date.split('/')]

        container = self.element.container
        language = folder.Language()
        # We run IRuleExecutor here to make sure other rules will be
        # executed for the newly created folders
        executor = IRuleExecutor(self.context, None)
        for fId in folderStructure:
            if not fId in folder.objectIds():
                _createObjectByType(container, folder, id=fId,
                                    title=fId, description=fId)
                folder = folder[fId]
                # this makes happy multilang sites
                folder.setLanguage(language)
                event = ObjectAddedEvent(folder, aq_parent(folder), fId)
                if executor is not None:
                    executor(event)
            else:
                folder = folder[fId]
        return folder


class GroupByDateAddForm(ActionAddForm):
    """
    An add form for the group by date action
    """
    schema = IGroupByDateAction
    label = _("Add group by date folder action")
    description = _("A content rules action to move an item to a folder"
                    " structure.")
    Type = GroupByDateAction

    # def create(self, data):
    #     a = GroupByDateAction()
    #     form.applyChanges(a, self.schema, data)
    #     return a


class GroupByDateAddFormView(ContentRuleFormWrapper):
    form = GroupByDateAddForm


class GroupByDateEditForm(ActionEditForm):
    """
    An edit form for the group by date action
    """
    schema = IGroupByDateAction
    label = _("Edit group by date action")
    description = _("A content rules action to move an item to a folder"
                    " structure.")
    form_name = _('Configure element')


class GroupByDateEditFormView(ContentRuleFormWrapper):
    form = GroupByDateEditForm
