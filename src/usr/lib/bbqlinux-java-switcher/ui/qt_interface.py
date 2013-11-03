#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
sys.path.append('/usr/lib/bbqlinux-java-switcher')
import os
import string

from switcher import SwitcherEngine

from PyQt4 import QtGui, QtCore, uic

class SwitcherWindow(QtGui.QMainWindow):

    JAVA_SLINK = "/usr/bin/java"
    JDK6_PATH = "/opt/java6/bin/java"
    OPENJDK7_PATH = "/usr/lib/jvm/java-7-openjdk/jre/bin/java"

    def __init__(self):
        # Check if we run as root
        if os.geteuid() != 0:
            sys.exit('Script must be run as root')

        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('/usr/share/bbqlinux-java-switcher/qt_interface.ui')

        # Set window title
        self.ui.setWindowTitle("BBQLinux Java Switcher")
        self.ui.setWindowIcon(QtGui.QIcon('/usr/share/bbqlinux/icons/bbqlinux_icon_blue_32x32.png'))

        # Show the window
        self.ui.show()
        
        # Move main window to center
        qr = self.ui.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())

        # Connect the buttons
        self.connect(self.ui.button_exit, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.button_jdk6, QtCore.SIGNAL("clicked()"), self.button_jdk6_clicked)
        self.connect(self.ui.button_openjdk7, QtCore.SIGNAL("clicked()"), self.button_openjdk7_clicked)

        # Refresh button states
        self.refresh_button_state()

    def refresh_button_state(self):
        python_path = self.get_active_java(self.JAVA_SLINK)
        if python_path == self.JDK6_PATH:
            self.ui.button_jdk6.setText(unicode("Active"))
            self.ui.button_jdk6.setEnabled(False)
            self.ui.button_openjdk7.setText(unicode("Activate"))
            self.ui.button_openjdk7.setEnabled(True)
        elif python_path == self.OPENJDK7_PATH:
            self.ui.button_openjdk7.setText(unicode("Active"))
            self.ui.button_openjdk7.setEnabled(False)
            self.ui.button_jdk6.setText(unicode("Activate"))
            self.ui.button_jdk6.setEnabled(True)
        else:
            self.ui.button_jdk6.setText(unicode("Activate"))
            self.ui.button_jdk6.setEnabled(True)
            self.ui.button_openjdk7.setText(unicode("Activate"))
            self.ui.button_openjdk7.setEnabled(True)

    def button_jdk6_clicked(self):
        os.system("rm %s" % self.JAVA_SLINK)
        os.system("ln -s %s %s" % (self.JDK6_PATH, self.JAVA_SLINK))
        self.refresh_button_state()

    def button_openjdk7_clicked(self):
        os.system("rm %s" % self.JAVA_SLINK)
        os.system("ln -s %s %s" % (self.OPENJDK7_PATH, self.JAVA_SLINK))
        self.refresh_button_state()

    def get_active_java(self, link):
        try:
            path = os.readlink(link)
            return path
        except Exception: 
            pass