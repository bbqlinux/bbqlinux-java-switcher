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

    BIN_PATH = "/usr/bin/"
    JDK6_JAVA_HOME = "/opt/java6"
    JDK6_PATH = "/opt/java6/bin/"
    JDK7_OPENJDK_JAVA_HOME = "/usr/lib/jvm/java-7-openjdk"
    JDK7_OPENJDK_PATH = "/usr/lib/jvm/java-7-openjdk/bin/"
    JRE7_OPENJDK_PATH = "/usr/lib/jvm/java-7-openjdk/jre/bin/"

    commands = ['java', 'javac', 'javadoc', 'javah', 'javap', 'javaws']

    PROFILE_FILE = '/etc/profile.d/override_java.sh'
    NOTICE = '\r\nJava version changed!\r\n\nWell, not completely...\r\nPlease source the following file in your bashrc:\r\n\n%s' % PROFILE_FILE

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
        cmd = "java"
        python_path = self.get_active_java("%s%s" % (self.BIN_PATH, cmd))
        if python_path == "%s%s" % (self.JDK6_PATH, cmd):
            self.ui.button_jdk6.setText(unicode("Active"))
            self.ui.button_jdk6.setEnabled(False)
            self.ui.button_openjdk7.setText(unicode("Activate"))
            self.ui.button_openjdk7.setEnabled(True)
        elif python_path == "%s%s" % (self.JRE7_OPENJDK_PATH, cmd):
            self.ui.button_openjdk7.setText(unicode("Active"))
            self.ui.button_openjdk7.setEnabled(False)
            self.ui.button_jdk6.setText(unicode("Activate"))
            self.ui.button_jdk6.setEnabled(True)
        else:
            self.ui.button_jdk6.setText(unicode("Activate"))
            self.ui.button_jdk6.setEnabled(True)
            self.ui.button_openjdk7.setText(unicode("Activate"))
            self.ui.button_openjdk7.setEnabled(True)

        # Disable buttons if binaries not found.
        for cmd in self.commands:
            # Check JDK6 binaries
            if not os.path.isfile(self.JDK6_PATH + cmd):
                self.ui.button_jdk6.setText(unicode("Not Found"))
                self.ui.button_jdk6.setEnabled(False)
                break
        for cmd in self.commands:
            # Check JDK7 binaries (using 2 for loops so we can utilize break)
            if cmd == 'java':
                if not os.path.isfile(self.JRE7_OPENJDK_PATH + cmd):
                    self.ui.button_openjdk7.setText(unicode("Not Found"))
                    self.ui.button_openjdk7.setEnabled(False)
                    break
            elif cmd == 'javaws':
                pass # JDK7 has no javaws
            else:
                if not os.path.isfile(self.JDK7_OPENJDK_PATH + cmd):
                    self.ui.button_openjdk7.setText(unicode("Not Found"))
                    self.ui.button_openjdk7.setEnabled(False)
                    break

    def button_jdk6_clicked(self):
        for cmd in self.commands:
            os.system("rm %s%s" % (self.BIN_PATH, cmd))
            os.system("ln -s %s%s %s%s" % (self.JDK6_PATH, cmd, self.BIN_PATH, cmd))

        os.system("echo 'export JAVA_HOME=%s' > %s" % (self.JDK6_JAVA_HOME, self.PROFILE_FILE))
        self.ui.noticeTextEdit.setText("%s" % self.NOTICE)
        self.refresh_button_state()

    def button_openjdk7_clicked(self):
        for cmd in self.commands:
            os.system("rm %s%s" % (self.BIN_PATH, cmd))
            if cmd == 'java':
                os.system("ln -s %s%s %s%s" % (self.JRE7_OPENJDK_PATH, cmd, self.BIN_PATH, cmd))
            else:
                os.system("ln -s %s%s %s%s" % (self.JDK7_OPENJDK_PATH, cmd, self.BIN_PATH, cmd))

        os.system("echo 'export JAVA_HOME=%s' > %s" % (self.JDK7_OPENJDK_JAVA_HOME, self.PROFILE_FILE))
        self.ui.noticeTextEdit.setText("%s" % self.NOTICE)
        self.refresh_button_state()

    def get_active_java(self, link):
        try:
            path = os.readlink(link)
            return path
        except Exception:
            pass
