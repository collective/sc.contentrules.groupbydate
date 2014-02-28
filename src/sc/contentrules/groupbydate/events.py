# -*- coding: utf-8 -*-
from zope.component.interfaces import IObjectEvent
from zope.interface import implements


class IObjectGroupedByDate(IObjectEvent):
    """ An event triggered when object gets grouped by date
    """


class ObjectGroupedByDate(object):
    implements(IObjectGroupedByDate)

    def __init__(self, obj):
        self.object = obj
