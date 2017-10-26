#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class LibiconvConan(ConanFile):
    name = "libiconv"
    version = "1.15"
    description = "Convert text to and from Unicode"
    license = "https://github.com/lz4/lz4/blob/master/lib/LICENSE"
    url = "https://github.com/bincrafters/conan-libiconv"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    lib_short_name = "libiconv"
    archive_name = "{0}-{1}".format(lib_short_name, version)
    install_dir = "libiconv-install"

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/libiconv"
        tools.get("{0}/{1}.tar.gz".format(source_url, self.archive_name))

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("msys2_installer/latest@bincrafters/stable")

    def build_autotools(self):
        env_build = AutoToolsBuildEnvironment(self)
        configure_args = ['--prefix=%s' % os.path.abspath(self.install_dir)]
        if self.options.shared:
            configure_args.extend(['--disable-static', '--enable-shared'])
        else:
            configure_args.extend(['--enable-static', '--disable-shared'])
        with tools.chdir(self.archive_name):
            env_build.configure(args=configure_args)
            env_build.make()
            env_build.make(args=["install"])

    def run_in_msys(self, command):
        bash = "%MSYS_ROOT%\\usr\\bin\\bash"
        vcvars_command = tools.vcvars_command(self.settings)
        self.run("{vcvars_command} && {bash} -c ^'{command}'".format(
            vcvars_command=vcvars_command,
            bash=bash,
            command=command))

    def build_vs(self):
        # README.windows
        if self.settings.arch == "x86":
            host = "i686-w64-mingw32"
        elif self.settings.arch == "x86_64":
            host = "x86_64-w64-mingw32"
        else:
            raise Exception("unsupported architecture %s" % self.settings.arch)
        prefix = tools.unix_path(os.path.abspath(self.install_dir))
        if self.options.shared:
            options = '--disable-static --enable-shared'
        else:
            options = '--enable-static --disable-shared'

        with tools.chdir(self.archive_name):
            # WORKAROUND
            tools.replace_in_file(os.path.join('build-aux', 'ar-lib'), 'MINGW*)', 'MSYS*)')
            tools.replace_in_file(os.path.join('build-aux', 'compile'), 'MINGW*)', 'MSYS*)')
            # WORKAROUND: libtool:   error: unrecognised option: '-DPACKAGE_VERSION_STRING=\"1.15\"'
            for d in ['src', 'lib']:
                tools.replace_in_file(os.path.join(d, 'Makefile.in'),
                                      '`$(SHELL) $(srcdir)/../windows/windres-options --escape $(PACKAGE_VERSION)`', '')
            package_version = self.version.split('.')
            package_version_major = package_version[0]
            package_version_minor = package_version[1]
            if len(package_version) > 2:
                package_version_subminor = package_version[2]
            else:
                package_version_subminor = '0'
            for res in ['iconv.rc', 'libiconv.rc']:
                tools.replace_in_file(os.path.join('windows', res),
                                      'PACKAGE_VERSION_MAJOR', package_version_major)
                tools.replace_in_file(os.path.join('windows', res),
                                      'PACKAGE_VERSION_MINOR', package_version_minor)
                tools.replace_in_file(os.path.join('windows', res),
                                      'PACKAGE_VERSION_SUBMINOR', package_version_subminor)
                tools.replace_in_file(os.path.join('windows', res),
                                      'PACKAGE_VERSION_STRING', '"%s"' % self.version)

            self.run_in_msys('chmod a+x build-aux/ar-lib build-aux/compile')
            self.run_in_msys('pacman -S make diffutils --noconfirm')

            self.run_in_msys('win32_target=_WIN32_WINNT_VISTA ./configure '
                             '{options} '
                             '--host={host} '
                             '--prefix={prefix} '
                             'CC="$PWD/build-aux/compile cl -nologo" '
                             'CFLAGS="-{runtime}" '
                             'CXX="$PWD/build-aux/compile cl -nologo" '
                             'CXXFLAGS="-{runtime}" '
                             'CPPFLAGS="-D_WIN32_WINNT=0x0600 -I{prefix}/include" '
                             'LDFLAGS="-L{prefix}/lib" '
                             'LD="link" '
                             'NM="dumpbin -symbols" '
                             'STRIP=":" '
                             'AR="$PWD/build-aux/ar-lib lib" '
                             'RANLIB=":" '.format(host=host, prefix=prefix, options=options,
                                                  runtime=str(self.settings.compiler.runtime)))

            self.run_in_msys('make -j{cpu_count}'.format(cpu_count=tools.cpu_count()))
            self.run_in_msys('make install')

    def build_mingw(self):
        raise Exception("not implemented")

    def build(self):
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self.build_vs()
            elif self.settings.compiler == "gcc":
                self.build_mingw()
            else:
                # TODO : clang on Windows and others
                raise Exception("unsupported build")
        else:
            self.build_autotools()

    def package(self):
        self.copy("COPYING", dst=".", src=self.archive_name)
        self.copy("*.h", dst="include", src=os.path.join(self.install_dir, "include"))
        if str(self.settings.os) in ["Macos", "iOS", "watchOS", "tvOS"]:
            if self.options.shared:
                self.copy("*.dylib", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            else:
                self.copy("*.a", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
        elif str(self.settings.os) in ["Linux", "Android"]:
            if self.options.shared:
                self.copy("*.so*", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            else:
                self.copy("*.a", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
        elif self.settings.os == "Windows":
            self.copy("*.lib", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            if self.options.shared:
                self.copy("*.dll", dst="bin", src=os.path.join(self.install_dir, "bin"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
