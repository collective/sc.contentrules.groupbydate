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

To do so, this package is installed in a Plone Site and a new content rule is
created. This content rule will be triggered by the publication of an News
Item and will initialize a '''Move an item to a date-based folder
structure'''.

This action has a target (/news) and a structure ('ymd'), so as our News Item,
with id hello-world, is published on the site, it will be moved to a a new
folder structure under /news. Supposing it's December 19th, 2008, the item
will end in /news/2009/12/19/hello-world.

Configuration
-------------

We will explain step by step how to config this case through plone user
interface.

1) You need go to site setup and then "content rules".
2) Click on "Add content rule".
3) Set the title and select "workflow state changed" in triggered event and
   save.
4) You will be redirected to the previous view but you will see the rule
   that you just added in a table. You will note that the title is a link.
   Click it.
5) Ok, in here you will note that you have two settable categories. Conditions
   and actions. To make this happen, you need to add two condition and one
   action. One of the condition must be related to the content type and the
   the other one to the workflow state of the object.
6) So, "content type" condition is selected by default. Just click the add
   button and then select "News item" and save.
7) To add the second condition, following the last step, you need to
   select "Workflow state" and then the state that correspond to publication.
   Could be "publish" or "publish_intenally".
8) Now is turn of the action. You will see that "Logger" is selected
   by default. You need to change it to "Move an item to a date-based folder
   structure". Click add.
9) You are now in the add form of the action. You will see four required
   fields. "Base folder" is the base folder for the date hierarchy. For this
   you have different ways to set it. You can search a folder in the text
   input field or select one of the dropdown menu.
   In the last one you will note and option called "One level up". This means
   that the folder structure date hierarchy will be done one level up of
   the content selected in which the rule will be applied. This will be useful
   when we have it to multiple types of contents in which each one are added
   in different folders.
   Also, we have the option "Same folder of content" which is obvious to
   understand. In this case select "News".
10) We can have in our site a different type besides Folder to keep content.
    The Container field basically give us the option to select what content
    type we are going to need to play the container role. In case that other
    type is selected, the structure will be based on this type instead of
    folders. We will leave this field selected is "Folder" which is the
    default.
11) Also, we can select the default view for each of this folders. You need
    to know the name of the view that you want. If the view doesn't exists,
    the form will be showing an error. We will leave this field as
    "folder_listing" which is the default.
12) In hierarchy structure we can choose the order. Use strftime formating.
    e.g.: '%Y/%m/%d' to have 2011/11/17 or '%Y/%m' to have 2011/11. Leave
    this field with default value.
13) Now you just need to apply this rule in the right place of the site. If you
    don't know how to do this, follow this link:

    * http://plone.org/documentation/kb/using-content-rules/applying-a-content-rule


