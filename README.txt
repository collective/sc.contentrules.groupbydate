***************************
sc.contentrules.groupbydate
***************************

.. contents:: Table of Contents
   :depth: 2

Overview
--------
sc.contentrules.groupbydate is a very basic content rule action used to
organize content under a chronological-based hierarchy on a web site upon
publication.

Base use case
-------------

A news portal with a few dozen new content items per day needs to organize its
information in a chronological, yet human-readable, hierarchy.

To do so this package is installed in a Plone Site and a new content rule is
created. This content rule will be triggered by the publication of an News
Item and will initialize a '''Move an item to a date-based folder
structure'''.

This action has a target (/news) and a structure ('ymd'), so as our News Item,
with id hello-world, is published on the site, it will be moved to a a new
folder structure under /news. Supposing it's December 19th, 2008, the item
will end in /news/2009/12/19/hello-world.

