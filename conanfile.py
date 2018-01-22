#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class LibiconvConan(ConanFile):
    name = "libiconv"
    version = "1.15"
    description = "Convert text to and from Unicode"
    url = "https://github.com/bincrafters/conan-libiconv"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    archive_name = "{0}-{1}".format(name, version)

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/libiconv"
        tools.get("{0}/{1}.tar.gz".format(source_url, self.archive_name))

    def build_autotools(self):
        prefix = os.path.abspath(self.package_folder)
        win_bash = False
        if self.settings.compiler == 'Visual Studio':
            prefix = tools.unix_path(prefix)
            win_bash = True

        env_build = AutoToolsBuildEnvironment(self, win_bash=win_bash)
        env_build.fpic = self.options.fPIC

        configure_args = ['--prefix=%s' % prefix]
        if self.options.shared:
            configure_args.extend(['--disable-static', '--enable-shared'])
        else:
            configure_args.extend(['--enable-static', '--disable-shared'])
        host = None

        env_vars = {}
        build = None
        if self.settings.compiler == 'Visual Studio':
            build = False
            if self.settings.arch == "x86":
                host = "i686-w64-mingw32"
            elif self.settings.arch == "x86_64":
                host = "x86_64-w64-mingw32"
            runtime = str(self.settings.compiler.runtime)
            configure_args.extend(['CC=$PWD/build-aux/compile cl -nologo',
                                   'CFLAGS=-%s' % runtime,
                                   'CXX=$PWD/build-aux/compile cl -nologo',
                                   'CXXFLAGS=-%s' % runtime,
                                   'CPPFLAGS=-D_WIN32_WINNT=0x0600 -I%s/include' % prefix,
                                   'LDFLAGS=-L%s/lib' % prefix,
                                   'LD=link',
                                   'NM=dumpbin -symbols',
                                   'STRIP=:',
                                   'AR=$PWD/build-aux/ar-lib lib',
                                   'RANLIB=:'])
            env_vars['win32_target'] = '_WIN32_WINNT_VISTA'

            with tools.chdir(self.archive_name):
                tools.run_in_windows_bash(self, 'chmod +x build-aux/ar-lib build-aux/compile')

        with tools.chdir(self.archive_name):
            with tools.environment_append(env_vars):
                env_build.configure(args=configure_args, host=host, build=build)
                if self.settings.compiler == 'Visual Studio':
                    self.run_in_cygwin('make')
                    self.run_in_cygwin('make install')
                else:
                    env_build.make()
                    env_build.make(args=["install"])

    def build_mingw(self):
        raise Exception("not implemented")

    def build(self):
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                cygwin_bin = self.deps_env_info['cygwin_installer'].CYGWIN_BIN
                with tools.environment_append({'PATH': [cygwin_bin],
                                               'CONAN_BASH_PATH': '%s/bash.exe' % cygwin_bin}):
                    with tools.vcvars(self.settings):
                        self.build_autotools()
            elif self.settings.compiler == "gcc":
                self.build_mingw()
            else:
                # TODO : clang on Windows and others
                raise Exception("unsupported build")
        else:
            self.build_autotools()

    def package(self):
        self.copy(os.path.join(self.archive_name, "COPYING.LIB"), dst="licenses", ignore_case=True, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and self.options.shared:
            self.cpp_info.libs = ['iconv.dll.lib']
        else:
            self.cpp_info.libs = ['iconv']
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
