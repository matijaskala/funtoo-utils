#!/usr/bin/python3

from merge_utils import *

gentoo_src = GitTree("gentoo", "master", "git://anongit.gentoo.org/repo/gentoo.git", pull=True)
funtoo_utils = Tree("funtoo-utils",os.path.abspath(".."))
party_overlay = GitTree("party-overlay", "master", "git://github.com/matijaskala/party-overlay.git", pull=True)
ubuntu_overlay = GitTree("ubuntu-overlay", "master", "git://github.com/matijaskala/ubuntu-overlay.git", pull=True)
stable_overlay = GitTree("stable-overlay", "master", "git://github.com/matijaskala/stable-overlay.git", pull=True)
funtoo_original_overlay = GitTree("funtoo-overlay", "master", "git://github.com/funtoo/funtoo-overlay.git", pull=True)
elementary_overlay = GitTree("elementary", "master", "git://github.com/pimvullers/elementary.git", pull=True)
sabayon_for_gentoo = GitTree("sabayon-for-gentoo", "master", "git://github.com/Sabayon/for-gentoo.git", pull=True)
sabayon_distro_src = GitTree("sabayon-distro", "master", "git://github.com/Sabayon/sabayon-distro.git", pull=True)
sabayon_tools = GitTree("sabayon-tools", "master", "git://github.com/fusion809/sabayon-tools.git", pull=True)
gamerlay = GitTree("gamerlay", "master", "git://anongit.gentoo.org/proj/gamerlay.git", pull=True)

steps = [
	GitCheckout("funtoo.org"),
	SyncFromTree(gentoo_src,exclude=["metadata/.gitignore", "/metadata/cache/**", "ChangeLog", "dev-util/metro"]),
	ApplyPatchSeries("%s/funtoo/patches" % party_overlay.root ),
	SyncDir(party_overlay.root, "profiles", exclude=["categories", "repo_name", "updates"]),
	MergeUpdates(party_overlay.root),
	SyncDir(party_overlay.root,"licenses"),
	SyncDir(party_overlay.root,"eclass"),
	InsertEbuilds(party_overlay, select="all", replace=True, merge=["dev-util/kdevelop", "dev-util/kdevplatform", "sys-devel/gcc", "sys-libs/glibc", "sys-libs/pam"]),
	InsertEbuilds(ubuntu_overlay, replace=True, merge=["gnome-base/gnome-desktop"]),
	InsertEbuilds(stable_overlay, replace=True),
	InsertEbuilds(elementary_overlay, select=["dev-libs/properties-cpp", "gnome-base/gnome-desktop", "gnome-base/gsettings-desktop-schemas"], skip=None, replace=False),
	InsertEbuilds(funtoo_original_overlay, select=["sys-kernel/debian-sources", "sys-kernel/openvz-rhel6-stable"], skip=None, replace=True),
	InsertEbuilds(sabayon_for_gentoo, select=["app-admin/equo", "app-admin/matter", "sys-apps/entropy", "sys-apps/entropy-server", "sys-apps/entropy-client-services","app-admin/rigo", "sys-apps/rigo-daemon", "sys-apps/magneto-core", "x11-misc/magneto-gtk", "x11-misc/magneto-gtk3", "kde-misc/magneto-kde", "app-misc/magneto-loader", "app-admin/authconfig", "dev-libs/libreport", "media-video/kazam", "net-misc/fcoe-utils", "net-misc/lldpad", "sys-apps/libhbalinux", "sys-auth/realmd"], replace=True),
        InsertEbuilds(sabayon_tools, select=["media-video/rage"]),
        InsertEbuilds(gamerlay),
	GenCache(),
	GenUseLocalDesc()
]

d = home+"git/ports-2013"
if not os.path.isdir(d):
	os.makedirs(d)
if not os.path.isdir("%s/.git" % d):
	runShell("( cd %s; git init )" % d )
	runShell("echo 'created by merge.py' > %s/README" % d )
	runShell("( cd %s; git add README; git commit -a -m 'initial commit by merge.py' )" % d )
	runShell("( cd %s; git checkout -b funtoo.org; git rm -f README; git commit -a -m 'initial funtoo.org commit' )" % ( d ) )
	print("Pushing disabled automatically because repository created from scratch.")
	push = False
prod = GitTree("prod", root=d)
prod.run(steps)
prod.gitCommit(message="updates by Skala",branch=push)
