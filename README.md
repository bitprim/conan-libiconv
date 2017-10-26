[![Build status](https://ci.appveyor.com/api/projects/status/n5bwli6x9ovqmvq4/branch/testing/1.15?svg=true)](https://ci.appveyor.com/project/BinCrafters/conan-libiconv/branch/testing/1.15)
[![Build Status](https://travis-ci.org/bincrafters/conan-libiconv.svg?branch=testing%2F1.15)](https://travis-ci.org/bincrafters/conan-libiconv)

# This repository holds a recipe for the libiconv unicode conversion library

[Conan.io](https://conan.io) package for [libiconv](https://www.gnu.org/software/libiconv) project

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/bincrafters/public-conan/libiconv%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install libiconv/1.5@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    libiconv/1.5@bincrafters/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..
	
Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git. 

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly. 

## Build  

This is a header only library, so nothing needs to be built.

## Package 

    $ conan create bincrafters/stable
	
## Add Remote

	$ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload libiconv/1.5@bincrafters/stable --all -r bincrafters

### License
[BSD 2-Clause](http://git.savannah.gnu.org/cgit/libiconv.git/tree/COPYING?h=v1.15)
