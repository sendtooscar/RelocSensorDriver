FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/RelocSensorDriver/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_lisp"
  "../msg_gen/lisp/Relocdata.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_Relocdata.lisp"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_lisp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
