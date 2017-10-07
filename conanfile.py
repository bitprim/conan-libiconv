from conans import ConanFile, tools, os


class LibiconvConan(ConanFile):
    name = "libiconv"
    version = "1.15"
    description = "Convert text to and from Unicode"
    license = "https://github.com/lz4/lz4/blob/master/lib/LICENSE"
    url = "https://github.com/bincrafters/conan-libiconv"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    lib_short_name = "libiconv"
    archive_name = "{0}-{1}".format(lib_short_name, version)
            
    def source(self):
        source_url = "https://ftp.gnu.org/gnu/libiconv"
        tools.get("{0}/{1}.tar.gz".format(source_url, self.archive_name))
                
    def build(self):   
        #if self.settings.os == "Linux":
        #if self.settings.os == "Darwin":
        if self.settings.os != "Windows":
            env_build = AutoToolsBuildEnvironment(self)
            configure_args = ['--prefix=%s' % self.install_dir]
            with tools.chdir(self.archive_name):
                env_build.configure(args=configure_args)
                env_build.make()
                env_build.make(args=["install"])
    
    def package(self):
        self.copy("COPYING", dst=".", src=self.archive_name)
        self.copy("*.h", dst="include", src=os.path.join(self.archive_name, "include"))
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.path.append(path.join(self.package_folder, "bin"))