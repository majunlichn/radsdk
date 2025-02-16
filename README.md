# radsdk

radsdk is a software development kit that contains common C/C++ libraries and tools.

radsdk is easy to setup and use. The repository provides build scripts to download, build and install libraries, with some prebuilt binaries to save you time.

# Usage

First, setup [microsoft/vcpkg](https://github.com/microsoft/vcpkg):

```powershell
git clone https://github.com/microsoft/vcpkg.git
# Run the bootstrap script:
cd vcpkg
.\bootstrap-vcpkg.bat # Linux: ./bootstrap-vcpkg.sh
# Configure the VCPKG_ROOT environment variable for convenience (use "/" as the directory separator even on Windows):
$env:VCPKG_ROOT="C:/path/to/vcpkg" # Linux: export VCPKG_ROOT="/path/to/vcpkg"
```

Some libraries with prebuilt binaries are aready included in the repo and don't need additional step to setup; for other libraries you need to execute the python script `setup.py` to download and extract, or clone and build from source:

```powershell
cd radsdk
# Configure CMake generator with the following environment variables:
$env:CMAKE_GENERATOR="Visual Studio 17 2022"
$env:CMAKE_GENERATOR_PLATFORM="x64"
# Execute setup.py to download, build and install the libraries/tools you want:
python setup.py vcpkg SDL mysql dependencywalker
# Configure the RADSDK_ROOT environment variable for convenience:
$env:RADSDK_ROOT="C:/path/to/radsdk" # Linux: export RADSDK_ROOT="/path/to/radsdk"
```

You can specify packages that need to be setup (if not specified all libraries and tools will be setup):

- vcpkg: clone and build from source, check `vcpkg.json` for the package names.
- SDL: includes [SDL3](https://github.com/libsdl-org/SDL) and [SDL3_mixer](https://github.com/libsdl-org/SDL_mixer), clone and build from source.
- [mysql](https://dev.mysql.com/downloads/connector/cpp/): download and extract.
- [dependencywalker](https://dependencywalker.com): download and extract.

To use the vcpkg libraries you need to configure `VCPKG_MANIFEST_DIR` and `VCPKG_INSTALLED_DIR` when execute CMake:

```powershell
cmake -S . -B build -D VCPKG_MANIFEST_DIR="$env:RADSDK_ROOT" -D VCPKG_INSTALLED_DIR="$env:RADSDK_ROOT/vcpkg_installed"
```
