FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/RelocSensorDriver/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/RelocSensorDriver/msg/__init__.py"
  "../src/RelocSensorDriver/msg/_Relocdata.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
