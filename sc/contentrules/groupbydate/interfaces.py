# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.interface import Interface
from zope.schema import Choice
from zope.schema import Text
from zope.schema import Bool

from zope.schema.interfaces import ISource, IContextSourceBinder

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.vocabularies.catalog import SearchableTextSource


from sc.contentrules.groupbydate import MessageFactory as _

class SearchableTS(object):
    implements(IContextSourceBinder)
    
    def __init__(self, query, default_query=None):
        self.query = query
        self.default_query = default_query
    
    def __call__(self, context):
        context = getattr(context, 'context', context)
        return SearchableTextSource(context, base_query=self.query.copy(),
                                    default_query=self.default_query)


class IGroupByDateAction(Interface):
    """Configuration available for this content rule
    """
    base_folder = Choice(title=_(u"Base folder"),
                        description=_(u"Choose the base folder for the date hierarchy."),
                        required=True,
                        source=SearchableTS({'is_folderish' : True},
                                                    default_query='path:')
                        )
    
    structure = Choice(title=_(u"Hierarchy structure"),
                        description=_(u"Choose hierarchy structure."),
                        required=True,
                        vocabulary='sc.contentrules.groupbydate.vocabulary.hierarchies',
                        )
    
