# -*- coding: utf-8 -*-
from zope.component.interfaces import IObjectEvent
from zope.interface import implementer


class IObjectGroupedByDate(IObjectEvent):
    """ An event triggered when object gets grouped by date
    """

@implementer(IObjectGroupedByDate)
class ObjectGroupedByDate(object):

    def __init__(self, obj):
        self.object = obj
