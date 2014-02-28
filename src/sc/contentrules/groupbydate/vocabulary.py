# -*- coding: utf-8 -*-
from plone.app.vocabularies.catalog import QuerySearchableTextSourceView
from plone.app.vocabularies.catalog import SearchableTextSource
from plone.app.vocabularies.terms import BrowsableTerm
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from sc.contentrules.groupbydate.config import RELPATHVOC
from zope.component import queryUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import logging

logger = logging.getLogger('sc.contentrules.groupbydate')


class RelPathSearchableTextSource(SearchableTextSource):
    """ A special case of a SearchableTextSource where we always support
        relative paths
    """
    def __contains__(self, value):
        """Return whether the value is available in this source
        """
        if not (value[0] == '.'):
            result = super(RelPathSearchableTextSource,
                           self).__contains__(value)
        else:
            result = True
        return result

    def search(self, query_string):
        """ Add relative paths to vocabulary
        """
        results = super(RelPathSearchableTextSource,
                        self).search(query_string)
        relPaths = RELPATHVOC.keys()
        results = relPaths + list(results)
        return (r for r in results)


class RelPathQSTSourceView(QuerySearchableTextSourceView):
    """ A special case of a QuerySearchableTextSourceView where we
        always support relative paths
    """
    def getTerm(self, value):
        if not (value[0] == '.'):
            return super(RelPathQSTSourceView, self).getTerm(value)
        terms = RELPATHVOC
        token = value
        title = terms.get(value, value)
        browse_token = parent_token = None
        return BrowsableTerm(value, token=token, title=title,
                             description=value,
                             browse_token=browse_token,
                             parent_token=parent_token)


class ContainerSearcher(object):
    """ Check for all availables/allowed-addable folderish
        content types in the site.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal_url = getToolByName(context, 'portal_url')
        site = portal_url.getPortalObject()
        pt = getToolByName(site, 'portal_types')
        # Use only Friendly Types
        util = queryUtility(IVocabularyFactory, 'plone.app.vocabularies.ReallyUserFriendlyTypes')
        types = util(context)
        types_ids = types.by_token.keys()
        folderish = []
        for type_id in types_ids:
            site_type = pt[type_id]
            if (site_type.global_allow) and (site_type.isConstructionAllowed(site)):
                term = types.by_token[type_id]
                site.invokeFactory(type_id, 'item')
                item = site['item']
                if IFolderish.providedBy(item):
                    folderish.append(term)
                del site['item']
        return SimpleVocabulary(folderish)

ContainerSearcherFactory = ContainerSearcher()
