# radsdk

A software development kit contains common C/C++ packages, easy to setup and use.

# Usage

Setup [microsoft/vcpkg](https://github.com/microsoft/vcpkg):

    ```powershell
    git clone https://github.com/microsoft/vcpkg.git
    # Run the bootstrap script:
    cd vcpkg
    .\bootstrap-vcpkg.bat # Linux: ./bootstrap-vcpkg.sh
    # Configure the VCPKG_ROOT environment variable:
    $env:VCPKG_ROOT="C:\path\to\vcpkg" # Linux: export VCPKG_ROOT="/path/to/vcpkg"
    ```

Download and build additional libraries:
```powershell
cd radsdk
# Configure CMake generator:
$env:CMAKE_GENERATOR="Visual Studio 17 2022"
$env:CMAKE_GENERATOR_PLATFORM="x64"
# Execute setup.py:
python setup.py
# Configure the RADSDK_ROOT environment variable for convenience:
$env:RADSDK_ROOT="C:\path\to\radsdk" # Linux: export RADSDK_ROOT="/path/to/radsdk"
```
Generate project files for CMake projects that dependent on vcpkg packages with manifest mode:
```powershell
cmake -S . -B build -D VCPKG_MANIFEST_DIR=$env:RADSDK_ROOT -D VCPKG_INSTALLED_DIR=$env:RADSDK_ROOT/vcpkg_installed
```
