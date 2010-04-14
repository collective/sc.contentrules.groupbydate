# -*- coding: utf-8 -*-

from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.app.schema.vocabulary import IVocabularyFactory

from sc.contentrules.groupbydate import MessageFactory as _

structures = (('ymd', _(u'Year/Month/Day')),
              ('ym', _(u'Year/Month')),
              ('y', _(u'Year')),
              )

class HierarchiesVocabulary(object):
    """Vocabulary factory listing available hierarchies
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []

        for key, title  in structures:
            terms.append(
                SimpleTerm(
                    key,
                    title=title)
                )

        return SimpleVocabulary(terms)

HierarchiesVocabularyFactory = HierarchiesVocabulary()
