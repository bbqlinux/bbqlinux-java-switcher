# Maintainer: Daniel Hillenbrand <codeworkx [at] bbqlinux [dot] org>

pkgname=bbqlinux-java-switcher
pkgver=1.1.0
pkgrel=2
pkgdesc="BBQLinux Java Switcher"
arch=('any')
url="https://github.com/bbqlinux/bbqlinux-java-switcher"
license=('GPL')
depends=('bbqlinux-artwork' 'python2' 'qt4' 'python2-pyqt4' 'gksu' 'java-runtime-common')

package() {
  cd "$pkgdir"

  install -Dm755 "$srcdir/usr/bin/bbqlinux-java-switcher" usr/bin/bbqlinux-java-switcher

  cp -R "$srcdir/usr/lib/" usr/lib
  cp -R "$srcdir/usr/share/" usr/share
}
