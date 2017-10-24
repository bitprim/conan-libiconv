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
                
    def build(self):
        if self.settings.os != "Windows":
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
