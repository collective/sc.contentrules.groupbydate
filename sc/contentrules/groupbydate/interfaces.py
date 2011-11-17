# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Text
from zope.schema import Bool
from zope.schema import TextLine

from zope.schema.interfaces import ISource, IContextSourceBinder

from sc.contentrules.groupbydate.vocabulary import RelPathSearchableTextSource as SearchableTextSource

from sc.contentrules.groupbydate import MessageFactory as _

class SearchableTS(object):
    implements(IContextSourceBinder)
    
    def __init__(self, query, default_query=None):
        self.query = query
        self.default_query = default_query
    
    def __call__(self, context):
        context = getattr(context, 'context', context)
        results = SearchableTextSource(context, base_query=self.query.copy(),
                                       default_query=self.default_query)
        return results


class IGroupByDateAction(Interface):
    """Configuration available for this content rule
    """
    base_folder = Choice(title=_(u"Base folder"),
                        description=_(u"Choose the base folder for the date hierarchy."),
                        required=True,
                        source=SearchableTS({'is_folderish' : True},
                                             default_query='path:')
                        )
    
    structure = TextLine(title=_(u"Hierarchy structure"),
                      description=_(u"Choose hierarchy structure. Use strftime formating. e.g.: '%Y/%m/%d' to have 2011/11/17 or '%Y/%m' to have 2011/11"),
                      required=True,
                      default=u'%Y/%m/%d',
                      )
    
