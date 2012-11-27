***************************
sc.contentrules.groupbydate
***************************

.. contents:: Table of Contents
   :depth: 2

Overview
--------

sc.contentrules.groupbydate is a content rule action used to organize content
under a chronological-based hierarchy on a web site.

The 2.0 series introduces a major refactoring of the code base and **is not
backwards compatible** with previous versions.

Base use case
-------------

A news portal with a few dozen new content items per day needs to organize its
information in a chronological, yet human-readable, hierarchy.

To do so, this package is installed in a Plone Site and a new content rule is
created. This content rule will be triggered by the publication of an News
Item and will initialize a '''Move an item to a date-based folder
structure'''.

This action has a *Base folder* (/news), a *Hierarchy Structure* ('%Y/%m/%d')
and a Container ('Folder'), so as our News Item, with id hello-world, is
published on the site, it will be moved to a a new folder structure under /news.
Supposing it's March 29th, 2012, the item will end in
/news/2012/03/29/hello-world.

.. note:: The containers **2012**, **03** and **29** will be created using the
          Folder content type -- as specified in Container field.

Using the action
-------------------

We will explain step by step how to config this case through plone user
interface.

    * In a Plone site, with this package installed, go to **Site Setup** and
      then click on "Content Rules".

    * Click on "Add content rule".

    * Set the title to something meaninful -- 'Organize published News Items'
      --, select "Workflow State Changed" in **Triggered Event** and save.

    * You will be redirected to the previous view but you will see the rule
      you added listed. Click on the title of the rule to edit it's properties.

    * Ok, in here you will note that you have two settable categories. Conditions
      and actions. To make this happen, you need to add two conditions and one
      action.

        * The first condition must be related to the content type. Select
          "News item" and save.

        * The second one to the workflow state of the object. Select
          "Publish".

    * Now is turn of the action. Select "Move an item to a date-based folder
      structure" and click add.

    * You are now in the add form for the action. You will see three required
      fields:

      * "Base folder" is the base folder for the date hierarchy. For this
        you have different ways to set it. You can search a folder in the text
        input field or select one of the dropdown menu. In the last one you will note
        and option called "One level up". This means that the folder structure date
        hierarchy will be done one level up of the content selected in which the rule
        will be applied. This will be useful when we have it to multiple types of
        contents in which each one are added in different folders. Also, we have the
        option "Same folder of content" which is obvious to understand. In this case
        select "News".

      * "Container" allows you to select the folderish content to be used to create
        the group by date structure. We suggest you to use "Folder", the default option.

      * "Hierarchy structure" allows you to choose the way the structure will be
        created. Use strftime formating. e.g.: '%Y/%m/%d' to have 2011/11/17 or '%Y/%m'
        to have 2011/11. Leave this field with default value.

    * Now you just need to apply this rule in the right place of the site. If you
      don't know how to do this, follow this `link`_.


Mostly Harmless
---------------

.. image:: https://secure.travis-ci.org/collective/sc.contentrules.groupbydate.png
    :target: http://travis-ci.org/collective/sc.contentrules.groupbydate

Have an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/sc.contentrules.groupbydate/issues

.. _`link`: http://plone.org/documentation/kb/using-content-rules/applying-a-content-rule
