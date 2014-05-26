#!/bin/bash

src=rsync://rsync.at.gentoo.org/gentoo-portage/

github_path=git@github.com:matijaskala
dir=~/.funtoo/git/source-trees
name=gentoo-x86
if [ ! -e $dir/$name ]; then
	(
		install -d $dir
		cd $dir
		git clone $github_path/$name
	)
fi
cd $dir/$name || exit 1

# Now, use rsync to write new changes directly on top of our working files. New files will be added, deprecated files will be deleted.
rsync --recursive --links --safe-links --perms --times --compress --force --whole-file --delete --timeout=180 --exclude=/.git --exclude=/metadata/cache/ --exclude=/distfiles --exclude=/local --exclude=/packages $src $dir/$name || exit 1
# the rsync command wiped our critical .gitignore file, so recreate it.
echo "distfiles/*" > .gitignore || exit 2
echo "packages/*" >> .gitignore || exit 3
echo >> metadata/layout.conf || exit 1
echo "# Thin manifests" >> metadata/layout.conf || exit 1
echo "thin-manifests = true" >> metadata/layout.conf || exit 1
echo "sign-manifests = false" >> metadata/layout.conf || exit 1
find -iname Manifest -exec sed -n -i -e "/DIST/p" {} \;
git add --all || exit 1
git commit -m "updates by Skala" || exit 1
git push || exit 1
