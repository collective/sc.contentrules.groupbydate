# -*- coding: utf-8 -*-

from zope.interface import Invalid

class ViewFail(Invalid):
    """ Exception to know if we have a invalid value in default_view.
    """
    pass