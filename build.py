#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_template_default, build_shared
import platform

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=False)

    for settings, options, env_vars, build_requires, reference in builder.items:
        if build_shared.get_os() == "Windows":
            build_requires.update({"*": ["cygwin_installer/2.9.0@bincrafters/stable"]})
    
    builder.run()

    