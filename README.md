# radsdk

A software development kit contains common C/C++ packages, easy to setup and use.

# Usage

CMake projects use vcpkg packages with manifest mode:

```
cmake -S . -B build -D VCPKG_MANIFEST_DIR=$RADSDK_PATH -D VCPKG_INSTALLED_DIR=$RADSDK_PATH/vcpkg_installed
```
