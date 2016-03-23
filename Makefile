install:
  mkdir -p $(DESTDIR)/usr
  cd $(DESTDIR)/usr
  [ -e portage/distfiles ] && mv portage/distfiles __portage_distfiles
  [ -e portage/packages ] && mv portage/packages __portage_packages
  [ -e portage/rpm ] && mv portage/rpm __portage_rpm
  [ -e portage ] && rm -rf portage
  git clone git://github.com/matijaskala/ports-2013.git portage
  [ -e __portage_distfiles ] && mv __portage_distfiles portage/distfiles
  [ -e __portage_packages ] && mv __portage_packages portage/packages
  [ -e __portage_rpm ] && mv __portage_rpm portage/rpm
