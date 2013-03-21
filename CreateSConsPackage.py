#!/usr/bin/python
#
# This script creates a Mac OS X .pkg installer for SCons from a SCons tarball passed on the command line.
#
#       e.g. python CreateSConsPackage.py scons-2.3.0.tar.gz
#

import atexit, os, sys, tempfile

if len(sys.argv) != 2:
    print "A SCons tarball must be passed as a command line parameter"
    exit(1)

sconsTarball = os.path.abspath(sys.argv[1])
if not os.path.exists(sconsTarball):
    print "The specified SCons tarball does not exist: %s" % sconsTarball
    exit(1)

# Read the version string from the tarball name
sconsVersion = os.path.basename(sconsTarball)[6:-7]
packageName = "SCons-%s" % sconsVersion

print "Creating Mac OS X package for SCons %s from tarball '%s' ..." % (sconsVersion, sconsTarball)

# This is where the contents of the SCons tarball are put on the target machine. The normal 'python setup.py install'
# process is then run from this location and the directory is subsequently deleted by the PostInstall script.
targetTempDirectory = "/tmp/SConsInstaller"

print "Creating package directory structure ..."
packageDirectory = "%s/SConsPackage" % tempfile.gettempdir()
installedDirectory = packageDirectory + targetTempDirectory
os.system("rm -rf %s && mkdir -p %s" % (installedDirectory, installedDirectory))

# Clean up package directory on exit
def cleanupPackageDirectory():
    os.system("rm -rf %s" % packageDirectory)
atexit.register(cleanupPackageDirectory)

print "Extracting and relocating SCons tarball ..."
if os.system("tar -C %s -xf %s && mv %s/scons-%s/* %s" % (installedDirectory, sconsTarball, installedDirectory, sconsVersion, installedDirectory)) != 0:
    print "*** Failed extracting and relocating SCons tarball ***"
    exit(1)

# Ensure the PostInstall script is executable
os.chmod("Scripts/PostInstall", 0755)

# Build the final package
print "Creating package with pkgbuild ..."
if os.system( \
    "xcrun pkgbuild \
    --quiet \
    --root %s \
    --install-location / \
    --ownership recommended \
    --identifier com.tigris.SCons.pkg \
    --scripts Scripts/ \
    \"%s.pkg\"" % (packageDirectory, packageName)) != 0:
    print "*** Failed creating package ***"
    exit(1)

print "Success, '%s.pkg' was created" % packageName
