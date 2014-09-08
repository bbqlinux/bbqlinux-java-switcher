#!/usr/bin/env python2
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
import subprocess

from PyQt4 import QtGui, QtCore, uic

JDK6_STRING = 'java-6-oracle'
OPENJDK7_STRING = 'java-7-openjdk'
OPENJDK8_STRING = 'java-8-openjdk'

class SwitcherWindow(QtGui.QMainWindow):

    global JDK6_STRING
    global OPENJDK7_STRING
    global OPENJDK8_STRING

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
        self.connect(self.ui.button_openjdk8, QtCore.SIGNAL("clicked()"), self.button_openjdk8_clicked)

        # Refresh button states
        self.refresh_button_state()

    def refresh_button_state(self):
        cur_java = self.get_default_java()

        if JDK6_STRING in cur_java:
            self.button_jdk6_active(True)
            self.button_openjdk7_active(False)
            self.button_openjdk8_active(False)
        elif OPENJDK7_STRING in cur_java:
            self.button_jdk6_active(False)
            self.button_openjdk7_active(True)
            self.button_openjdk8_active(False)
        elif OPENJDK8_STRING in cur_java:
            self.button_jdk6_active(False)
            self.button_openjdk7_active(False)
            self.button_openjdk8_active(True)
        else:
            self.button_jdk6_active(False)
            self.button_openjdk7_active(False)
            self.button_openjdk8_active(False)

        # Disable buttons if binaries not found.
        java_supported = self.get_supported_java()

        if not JDK6_STRING in java_supported:
            self.ui.button_jdk6.setText(unicode("Not Found"))
            self.ui.button_jdk6.setEnabled(False)

        if not OPENJDK7_STRING in java_supported:
            self.ui.button_openjdk7.setText(unicode("Not Found"))
            self.ui.button_openjdk7.setEnabled(False)

        if not OPENJDK8_STRING in java_supported:
            self.ui.button_openjdk8.setText(unicode("Not Found"))
            self.ui.button_openjdk8.setEnabled(False)



    # ORACLE JAVA 6
    def button_jdk6_clicked(self):
        os.system("archlinux-java set %s" % (JDK6_STRING))
        self.refresh_button_state()

    def button_jdk6_active(self, state):
        if state == True:
            self.ui.button_jdk6.setText(unicode("Active"))
            self.ui.button_jdk6.setEnabled(False)
        else:
            self.ui.button_jdk6.setText(unicode("Activate"))
            self.ui.button_jdk6.setEnabled(True)

    # OPENJDK 7
    def button_openjdk7_clicked(self):
        os.system("archlinux-java set %s" % (OPENJDK7_STRING))
        self.refresh_button_state()

    def button_openjdk7_active(self, state):
        if state == True:
            self.ui.button_openjdk7.setText(unicode("Active"))
            self.ui.button_openjdk7.setEnabled(False)
        else:
            self.ui.button_openjdk7.setText(unicode("Activate"))
            self.ui.button_openjdk7.setEnabled(True)

    # OPENJDK 8
    def button_openjdk8_clicked(self):
        os.system("archlinux-java set %s" % (OPENJDK8_STRING))
        self.refresh_button_state()


    def button_openjdk8_active(self, state):
        if state == True:
            self.ui.button_openjdk8.setText(unicode("Active"))
            self.ui.button_openjdk8.setEnabled(False)
        else:
            self.ui.button_openjdk8.setText(unicode("Activate"))
            self.ui.button_openjdk8.setEnabled(True)



    def get_default_java(self):
        try:
            p1 = subprocess.Popen(['archlinux-java', 'get'], stdout=subprocess.PIPE)
            output = p1.communicate()[0]
            print("Default Java: %s" % output)
            self.ui.noticeTextEdit.setText(unicode("Default Java: %s" % output))
            return output
        except:
            print "Unexpected error:", sys.exc_info()[1]
            pass
   
    def get_supported_java(self):
        try:
            p1 = subprocess.Popen(['archlinux-java', 'status'], stdout=subprocess.PIPE)
            output = p1.communicate()[0]
            print("Supported Java: %s" % output)
            return output
        except:
            print "Unexpected error:", sys.exc_info()[1]
            pass
