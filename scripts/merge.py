#!/usr/bin/python2

from merge_utils import *

# Progress overlay merge
if not os.path.exists("/usr/bin/svn"):
	print("svn binary not found at /usr/bin/svn. Exiting.")
	sys.exit(1)

gentoo_src = Tree("gentoo-x86", "gentoo.org", "git://github.com/matijaskala/gentoo-x86.git", pull=True)
funtoo_utils = DeadTree("funtoo-utils",os.path.abspath(".."))
party_overlay = Tree("party-overlay", branch, "git://github.com/matijaskala/party-overlay.git", pull=True)
funtoo_original_overlay = Tree("funtoo-overlay", branch, "git://github.com/funtoo/funtoo-overlay.git", pull=True)
elementary_overlay = Tree("elementary", "master", "git://github.com/pimvullers/elementary.git", pull=True)
sabayon_for_gentoo = Tree("sabayon-for-gentoo", "master", "git://github.com/Sabayon/for-gentoo.git", pull=True)

funtoo_original_packages = [
	"app-dicts/dictd-moby-thesaurus",
	"app-portage/genlop",
	"mail-mta/postfix",
	"sys-cluster/vzctl",
	"sys-kernel/debian-sources",
	"sys-kernel/dkms",
	"sys-kernel/openvz-rhel6-stable",
]

partylinux_merge_packages = [
	"dev-util/kdevelop",
	"dev-util/kdevplatform",
	"sys-apps/systemd",
	"sys-devel/gcc",
	"x11-libs/cairo",
]

steps = [
	SyncTree(gentoo_src,exclude=["/metadata/cache/**", "CVS", "ChangeLog", "dev-util/metro"]),
	ApplyPatchSeries("%s/funtoo/patches" % party_overlay.root ),
	ThirdPartyMirrors(),
	SyncDir(party_overlay.root, "profiles", exclude=["categories", "default", "repo_name", "updates", "package.mask/party-compat"]),
	MergeUpdates(party_overlay.root),
	ProfileDepFix(),
	SyncDir(party_overlay.root,"licenses"),
	SyncDir(party_overlay.root,"eclass"),
	SyncFiles(funtoo_utils.root, {
		"data/layout.conf":"metadata/layout.conf",
		"data/gitignore":".gitignore",
	}),
	InsertEbuilds(party_overlay, select="all", skip=funtoo_original_packages, replace=True, merge=partylinux_merge_packages),
	InsertEbuilds(elementary_overlay, select=["dev-libs/properties-cpp", "gnome-base/gnome-desktop", "gnome-base/gsettings-desktop-schemas", "x11-libs/gtk+"], skip=None, replace=True, merge=["gnome-base/gnome-desktop"]),
	InsertEbuilds(funtoo_original_overlay, select=funtoo_original_packages, skip=None, replace=True),
	InsertEbuilds(sabayon_for_gentoo, select=["app-admin/equo", "app-admin/matter", "sys-apps/entropy", "sys-apps/entropy-server", "sys-apps/entropy-client-services","app-admin/rigo", "sys-apps/rigo-daemon", "sys-apps/magneto-core", "x11-misc/magneto-gtk", "x11-misc/magneto-gtk3", "kde-misc/magneto-kde", "app-misc/magneto-loader"], replace=True),
	ApplyPatchSeries("%s/partylinux/patches" % party_overlay.root ),
	Minify(),
	GenCache(),
	GenUseLocalDesc()
]

# work tree is a non-git tree in tmpfs for enhanced performance - we do all the heavy lifting there:

work = UnifiedTree(home+"work/merge-%s" % os.path.basename(dest[0]),steps)
work.run()

steps = [
	GitPrep("funtoo.org"),
	SyncTree(work)
]

# then for the production tree, we rsync all changes on top of our prod git tree and commit:

for d in dest:
	if not os.path.isdir(d):
		os.makedirs(d)
	if not os.path.isdir("%s/.git" % d):
		runShell("( cd %s; git init )" % d )
		runShell("echo 'created by merge.py' > %s/README" % d )
		runShell("( cd %s; git add README; git commit -a -m 'initial commit by merge.py' )" % d )
		runShell("( cd %s; git checkout -b funtoo.org; git rm -f README; git commit -a -m 'initial funtoo.org commit' )" % ( d ) )
		print("Pushing disabled automatically because repository created from scratch.")
		push = False
	prod = UnifiedTree(d,steps)
	prod.run()
	prod.gitCommit(message="updates by Skala",push=push)
