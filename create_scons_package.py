#!/usr/bin/python
#
# This script creates a Mac OS X .pkg installer for SCons from a SCons tarball
# passed on the command line.
#
#       e.g. python create_scons_package.py scons-2.4.0.tar.gz
#

import os
import sys
import tempfile

if len(sys.argv) != 2:
    print 'Error: A SCons tarball must be passed as a command line argument'
    exit(1)

tarball = os.path.abspath(sys.argv[1])
if not os.path.exists(tarball):
    print 'Error: The specified SCons tarball does not exist: %s' % tarball
    exit(1)

# Read the version string from the tarball name
version = os.path.basename(tarball)[6:-7]
package_name = 'SCons-%s' % version

# The SCons tarball's contents are put into /tmp/SConsInstaller on the target
# machine and then the normal 'python setup.py install' process is then run
# from there. The directory is subsequently deleted by the postinstall script.
package_directory = tempfile.gettempdir()
target_directory = package_directory + '/tmp/SConsInstaller'
os.system('mkdir -p %s' % target_directory)

# Extract tarball
if os.system('tar -C %s --strip-components 1 -xzf %s' %
             (target_directory, tarball)) != 0:
    print 'Error: Failed extracting SCons tarball'
    exit(1)

# Build the package
if os.system('xcrun pkgbuild --quiet --identifier com.scons.SCons.pkg \
              --install-location / --root %s --scripts Scripts/ "%s.pkg"' %
             (package_directory, package_name)) != 0:
    print 'Error: Failed creating package'
    exit(1)

# Cleanup
os.system('rm -rf %s' % package_directory)

print 'Success, %s.pkg was created' % package_name
