#!/usr/bin/python
#
# This script creates a Mac OS X .pkg installer for SCons from a SCons tarball
# passed on the command line.
#
#       e.g. python create_scons_package.py scons-2.4.0.tar.gz
#

import atexit
import os
import shutil
import sys
import tempfile

if len(sys.argv) != 2:
    print('Error: A SCons tarball must be passed as a command line argument')
    exit(1)

tarball = os.path.abspath(sys.argv[1])
if not os.path.exists(tarball):
    print('Error: The specified SCons tarball does not exist: %s' % tarball)
    exit(1)

# Read the version string from the tarball name
version = os.path.basename(tarball)[6:-7]
package_name = 'SCons-%s' % version

# Temporary directory to create the installer package in
package_directory = tempfile.mkdtemp()
def cleanup():
    shutil.rmtree(package_directory)
atexit.register(cleanup)

# The SCons tarball's contents are put into /tmp/SConsInstaller on the target
# machine and then the normal 'python setup.py install' process is then run
# from there. The directory is subsequently deleted by the postinstall script.
target_directory = package_directory + '/tmp/SConsInstaller'
os.makedirs(target_directory)

# Extract tarball
if os.system('tar -C %s --strip-components 1 -xzf %s' %
             (target_directory, tarball)) != 0:
    print('Error: Failed extracting SCons tarball')
    exit(1)

# Build the package
if os.system('xcrun pkgbuild --quiet --identifier com.scons.SCons.pkg \
              --install-location / --root %s --scripts scripts "%s.pkg"' %
             (package_directory, package_name)) != 0:
    print('Error: Failed creating package')
    exit(1)

print('Success, %s.pkg was created' % package_name)
