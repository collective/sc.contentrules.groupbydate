# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.interface import invariant

from zope.schema import Choice
from zope.schema import TextLine

from zope.schema.interfaces import IContextSourceBinder

from zope.app.component.hooks import getSite

from plone.directives import form

from sc.contentrules.groupbydate.vocabulary import RelPathSearchableTextSource as SearchableTextSource
from sc.contentrules.groupbydate.exceptions import ViewFail
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


class IGroupByDateAction(form.Schema):
    """ Configuration available for this content rule
    """
    base_folder = Choice(title=_(u"Base folder"),
                        description=_(u"Choose the base folder for the date hierarchy."),
                        required=True,
                        source=SearchableTS({'is_folderish': True},
                                             default_query='path:')
                        )

    container = Choice(title=u"Container",
                       description=_(u"Select the type of container in which the structure will be based."),
                       source='sc.contentrules.groupbydate.vocabulary.containers',
                       default='Folder',
                       required=True,
                       )

    default_view = TextLine(title=_(u"Default View"),
                      description=_(u"Default view that container will be render."),
                      default=u'folder_listing',
                      required=True,
                      )

    structure = TextLine(title=_(u"Hierarchy structure"),
                      description=_(u"Choose hierarchy structure. Use strftime formating. e.g.: '%Y/%m/%d' to have 2011/11/17 or '%Y/%m' to have 2011/11"),
                      required=True,
                      default=u'%Y/%m/%d',
                      )

    @invariant
    def validate_view(rule_form):
        """ A validator to check if the view is available for that
            container
        """
        portal = getSite()
        pt = portal.portal_types
        container = rule_form.container
        view = rule_form.default_view
        factory = pt[container]
        if not view in factory.view_methods:
            raise ViewFail
