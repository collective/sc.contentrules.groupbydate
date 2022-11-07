# -*- coding: utf-8 -*-
from sc.contentrules.groupbydate import MessageFactory as _
from sc.contentrules.groupbydate.vocabulary import (RelPathSearchableTextSource as
                                                    SearchableTextSource)
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import TextLine
from zope.schema.interfaces import IContextSourceBinder
from plone.app.vocabularies.catalog import CatalogSource


@implementer(IContextSourceBinder)
class SearchableTS(object):

    def __init__(self, query, default_query=None):
        self.query = query
        self.default_query = default_query

    def __call__(self, context):
        context = getattr(context, 'context', context)
        results = SearchableTextSource(context, base_query=self.query.copy(),
                                       default_query=self.default_query)
        return results


class IGroupByDateAction(Interface):
    """ Configuration options for this content rule action
    """
    base_folder = Choice(title=_(u"Base folder"),
                         description=_(u"Choose the base folder for the date "
                                       u"hierarchy."),
                         required=True,
                         source=CatalogSource(is_folderish=True),
                         )

    container = TextLine(title=_(u"Container"),
                         description=_(u"Select the type of container in which "
                                       u"the structure will be based."),
                         default=u'Folder',
                         required=True)

    structure = TextLine(title=_(u"Hierarchy structure"),
                         description=_(u"Choose hierarchy structure. Use "
                                       u"strftime formating. e.g.: '%Y/%m/%d'"
                                       u" to have 2011/11/17 or '%Y/%m' to "
                                       u"have 2011/11"),
                         required=True,
                         default=u'%Y/%m/%d')
