# -*- coding: utf-8 -*-
import itertools
from zope.interface import implements

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.vocabularies.catalog import SearchableTextSource
from plone.app.vocabularies.catalog import QuerySearchableTextSourceView
from plone.app.vocabularies.terms import BrowsableTerm

from zope.app.form.browser.interfaces import ISourceQueryView, ITerms

from zope.app.schema.vocabulary import IVocabularyFactory
from sc.contentrules.groupbydate.config import RELPATHVOC
from sc.contentrules.groupbydate.config import STRUCTURES

from sc.contentrules.groupbydate import MessageFactory as _


class HierarchiesVocabulary(object):
    """Vocabulary factory listing available hierarchies
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []

        for key, title  in STRUCTURES:
            terms.append(
                SimpleTerm(
                    key,
                    title=title)
                )

        return SimpleVocabulary(terms)

HierarchiesVocabularyFactory = HierarchiesVocabulary()

class RelPathSearchableTextSource(SearchableTextSource):
    """ A special case of a SearchableTextSource where we always support
        relative paths
    """
    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if not (value[0] == '.'):
            result = super(RelPathSearchableTextSource,self).__contains__(value)
        else:
            result = True
        return result
    
    def search(self, query_string):
        """ Add relative paths to vocabulary
        """
        results = super(RelPathSearchableTextSource,self).search(query_string)
        relPaths = RELPATHVOC.keys()
        results = relPaths + list(results)
        return (r for r in results)
    

class RelPathQSTSourceView(QuerySearchableTextSourceView):
    """ A special case of a QuerySearchableTextSourceView where we always support
        relative paths
    """
    def getTerm(self, value):
        if not (value[0] == '.'):
            return super(RelPathQSTSourceView,self).getTerm(value)
        terms = RELPATHVOC
        token = value
        title = terms.get(value,value)
        browse_token = parent_token = None
        return BrowsableTerm(value, token=token, title=title, 
                                 description=value,
                                 browse_token=browse_token,
                                 parent_token=parent_token)
        
    
