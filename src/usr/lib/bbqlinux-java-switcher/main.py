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
import argparse
import commands
import os
from PyQt4 import QtGui, QtCore, uic
from ui.qt_interface import SwitcherWindow

# main entry
if __name__ == "__main__":
    # CLI
    cliparser = argparse.ArgumentParser(description='Switch between JDK6 and OpenJDK7.')
    cliparser.add_argument("-6", "--jdk6", help="Enables JDK6", action="store_true")
    cliparser.add_argument("-7", "--openjdk7", help="Enables OpenJDK7", action="store_true")
    
    cliargs = cliparser.parse_args()
    if cliargs.jdk6 and cliargs.openjdk7:
        print("Error: Multiple versions specified. Please choose one version to switch to.")
        sys.exit(1)
    if cliargs.jdk6:
        # First let's check if all the binaries exist, if not exit, printing which aren't found
        missing_binaries = False # If this is set to True, binaries are missing and we will exit
        for cmd in SwitcherWindow.commands:
            if not os.path.isfile(SwitcherWindow.JDK6_PATH + cmd):
                missing_binaries = True
                print("Error: The binary %s%s was not found!" % (SwitcherWindow.JDK6_PATH, cmd))
        if missing_binaries: # Exit if binaries are missing
            print("Error: Exiting without switching due to missing binaries.")
            sys.exit(1)
            
        for cmd in SwitcherWindow.commands:
            os.system("rm %s%s" % (SwitcherWindow.BIN_PATH, cmd))
            os.system("ln -s %s%s %s%s" % (SwitcherWindow.JDK6_PATH, cmd, SwitcherWindow.BIN_PATH, cmd))

        print("%s%s \r\n" % (SwitcherWindow.NOTICE, SwitcherWindow.JDK6_JAVA_HOME))
        sys.exit(0)
    if cliargs.openjdk7:
        # First let's check if all the binaries exist, if not exit, printing which aren't found
        missing_binaries = False # If this is set to True, binaries are missing and we will exit
        for cmd in SwitcherWindow.commands:
            if cmd == 'java':
                if not os.path.isfile(SwitcherWindow.JRE7_OPENJDK_PATH + cmd):
                    missing_binaries = True
                    print("Error: The binary %s%s was not found!" % (SwitcherWindow.JRE7_OPENJDK_PATH, cmd))
            elif cmd == 'javaws':
                pass # JDK7 has no javaws
            else:
                if not os.path.isfile(SwitcherWindow.JDK7_OPENJDK_PATH + cmd):
                    missing_binaries = True
                    print("Error: The binary %s%s was not found!" % (SwitcherWindow.JDK7_OPENJDK_PATH, cmd))
        if missing_binaries:
            print("Error: Exiting without switching due to missing binaries.")
            sys.exit(1)

        for cmd in SwitcherWindow.commands:
            os.system("rm %s%s" % (SwitcherWindow.BIN_PATH, cmd))
            if cmd == 'java':
                os.system("ln -s %s%s %s%s" % (SwitcherWindow.JRE7_OPENJDK_PATH, cmd, SwitcherWindow.BIN_PATH, cmd))
            else:
                os.system("ln -s %s%s %s%s" % (SwitcherWindow.JDK7_OPENJDK_PATH, cmd, SwitcherWindow.BIN_PATH, cmd))

        print("%s%s \r\n" % (SwitcherWindow.NOTICE, SwitcherWindow.JDK7_OPENJDK_JAVA_HOME))
        sys.exit(0)
    
    # GUI
    app = QtGui.QApplication(sys.argv)
    win = SwitcherWindow()
    sys.exit(app.exec_())
