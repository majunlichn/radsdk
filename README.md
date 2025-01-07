# radsdk

radsdk is a software development kit that contains common C/C++ libraries.

radsdk is easy to setup and use. The repository provides build scripts to download, build and install libraries, with some prebuilt binaries to save you time.

# Usage

First, setup [microsoft/vcpkg](https://github.com/microsoft/vcpkg):

```powershell
git clone https://github.com/microsoft/vcpkg.git
# Run the bootstrap script:
cd vcpkg
.\bootstrap-vcpkg.bat # Linux: ./bootstrap-vcpkg.sh
# Configure the VCPKG_ROOT environment variable for convenience:
$env:VCPKG_ROOT="C:\path\to\vcpkg" # Linux: export VCPKG_ROOT="/path/to/vcpkg"
```

Then download and build the libraries by executing the python script `setup.py`:

```powershell
cd radsdk
# Configure CMake generator with the following environment variables:
$env:CMAKE_GENERATOR="Visual Studio 17 2022"
$env:CMAKE_GENERATOR_PLATFORM="x64"
# Execute setup.py to download, build and install the libraries:
python setup.py
# Configure the RADSDK_ROOT environment variable for convenience:
$env:RADSDK_ROOT="C:\path\to\radsdk" # Linux: export RADSDK_ROOT="/path/to/radsdk"
```

To use the vcpkg libraries you need to configure `VCPKG_MANIFEST_DIR` and `VCPKG_INSTALLED_DIR`:

```powershell
cmake -S . -B build -D VCPKG_MANIFEST_DIR="$env:RADSDK_ROOT" -D VCPKG_INSTALLED_DIR="$env:RADSDK_ROOT/vcpkg_installed"
```
