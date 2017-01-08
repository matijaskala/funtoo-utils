funtoo-utils
============
To generate a portage tree, execute scripts/merge.py

The tree will be generated at ~/.funtoo/ports-2013

If you want to generate it somewhere else:
- open scripts/merge.py
- look for the line that says 'd = home+"git/ports-2013"'
- change it to the desired location (for example: 'd = "/var/git/ports-2013"')
