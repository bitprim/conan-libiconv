# #!/usr/bin/env python
# # -*- coding: utf-8 -*-



from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="stable", archs=["x86_64"])
    builder.add_common_builds(shared_option_name="libiconv:shared", pure_c=True)

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if (settings["build_type"] == "Release" or settings["build_type"] == "Debug") \
                and not options["libiconv:shared"]:

            filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()


# #!/usr/bin/env python
# # -*- coding: utf-8 -*-


# from bincrafters import build_template_default, build_shared
# import platform

# if __name__ == "__main__":

#     builder = build_template_default.get_builder(pure_c=False)

#     for settings, options, env_vars, build_requires, reference in builder.items:
#         if build_shared.get_os() == "Windows":
#             build_requires.update({"*": ["cygwin_installer/2.9.0@bitprim/stable"]})
    
#     builder.run()

    