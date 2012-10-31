#!/bin/bash
# kudos to Products.Ploneboard for the base for this file
# ensure that when something is wrong, nothing is broken more than it should...
set -e

BASEDIR=src/sc/contentrules/groupbydate
LOCALES=$BASEDIR/locales

# first, create some pot containing anything
i18ndude rebuild-pot --pot $LOCALES/sc.contentrules.groupbydate.pot --create sc.contentrules.groupbydate --merge $LOCALES/manual.pot $BASEDIR

# finally, update the po files
i18ndude sync --pot $LOCALES/sc.contentrules.groupbydate.pot  `find . -iregex '.*sc.contentrules.groupbydate\.po$'|grep -v plone`

