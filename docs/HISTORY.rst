Changelog
---------

2.0.2 (unreleased)
^^^^^^^^^^^^^^^^^^^

- Nothing changed yet.


2.0.1 (2014-03-10)
^^^^^^^^^^^^^^^^^^

- Dexterity content types are now listed as options to folder creation
  [ericof]

- Code cleanup
  [ericof]


2.0 (2013-04-13)
^^^^^^^^^^^^^^^^^^^

- Plone 4.3 supported
  [ericof]

- Update translations, add italian traslation
  [simahawk]

- Update README and move to rst
  [simahawk]


2.0b2 (2012-11-30)
^^^^^^^^^^^^^^^^^^

- Execute IRuleExecutor for each folder created. This enables cascading content rules
  to be applied to newly created folders.
  [ericof]


2.0b1 (2012-11-27)
^^^^^^^^^^^^^^^^^^

- This package no longer needs to be installed in the site's control panel.
  [ericof]

- Removed the option to set the default layout for newly created folders.
  We suggest using sc.contentrules.layout for that.
  [ericof]

- Improved test coverage
  [ericof]

- PEP8 all over the code
  [ericof]

1.3b4 (2012-07-24)
^^^^^^^^^^^^^^^^^^

- Fix a performance issue with updating role mappings in portals with a huge
  amount of content already created [ericof]


1.3b3 (2012-07-10)
^^^^^^^^^^^^^^^^^^

- Removed dependency on plone.directives.form introduced on previous release.
  [aleGpereira]


1.3b2 (2012-07-03)
^^^^^^^^^^^^^^^^^^

- Default value for container field in schema was creating problems. Updating
  this value. [aleGpereira]

- Fix a little bug for container searcher vocabulary class. [aleGpereira]


1.3b1 (2012-06-21)
^^^^^^^^^^^^^^^^^^

- Added Spanish and updated Brazilian Portuguese translations. [hvelarde]

- Tested Plone 4.2 compatibility (fixes `#1`_). [hvelarde]

- Fixed package declaration and updated documentation. [hvelarde]

- Adding option so user can select the content type used as container.
  [aleGpereira]

- Adding a field to set a prefer view method for container. [aleGpereira]

- Adding integrational and functional test for view validator and container
  object creation. [aleGpereira]

- Update README documentation. [aleGpereira]


1.2 (2011-12-06)
^^^^^^^^^^^^^^^^

- Move testing to plone.app.testing [ericof]

- Fix Dublin Core support [ericof]

- Fix permissions for pt-br [lepri]


1.1.1 (2011-08-22)
^^^^^^^^^^^^^^^^^^

- Fix permission for Plone 4.x [cleberjsantos]


1.1 (2011-06-23)
^^^^^^^^^^^^^^^^

- Added z3c.autoinclude entry point to mark this as a Plone plugin
  [erico_andrei]

- Support for Plone 4.1.x [erico_andrei]


1.0 (2010-07-02)
^^^^^^^^^^^^^^^^

- Allow relative paths as base_folder [erico_andrei]

- Allow inputing of strftime formatting for structure field [erico_andrei]

- Add dependency of placeful workflow as we need it to avoid publishing
  content in an unpublished structure [erico_andrei]


0.5 (2009-07-28)
^^^^^^^^^^^^^^^^

- Very earlier i18n support [erico_andrei]

- Initial release

.. _`#1`: https://github.com/collective/sc.contentrules.groupbydate/issues/1
