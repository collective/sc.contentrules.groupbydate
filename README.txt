.. contents:: Table of Contents
   :depth: 2

sc.contentrules.groupbydate
***************************

Overview
--------
    sc.contentrules.groupbydate is a very basic content rule action used to 
    organize content under a chronological-based hierarchy on a web site upon
    publication.

Base use case
-------------
    
    A news portal with a few dozen new content items per day needs to organize 
    its information in a chronological, yet human-readable, hierarchy.
    
    To do so this package is installed in a Plone Site and a new content rule is
    created. This content rule will be triggered by the publication of an News
    Item and will initialize a '''Move an item to a date-based folder 
    structure'''. 
    
    This action has a target (/news) and a structure ('ymd'), so as our News 
    Item, with id hello-world, is published on the site, it will be moved to a 
    a new folder structure under /news. Supposing it's December 19th, 2008, the
    item will end in /news/2009/12/19/hello-world.

Requirements
------------

    * Plone 3.1 and above (http://plone.org/products/plone)
    
    * Products.CMFPlacefulWorkflow (http://plone.org/products/plone)
    
Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.contentrules.groupbydate``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            sc.contentrules.groupbydate

    2. Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

        [instance]
        ...
        zcml = 
            ...
            sc.contentrules.groupbydate
    

If another package depends on the sc.contentrules.groupbydate egg or 
includes its zcml directly you do not need to specify anything in the 
buildout configuration: buildout will detect this automatically.

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Sponsoring
----------

Development of this product was sponsored by `Simples Consultoria 
<http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * Erico Andrei (erico at simplesconsultoria dot com dot br)
