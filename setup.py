import os
import sys
import platform
import subprocess
import shutil
import urllib.request
from zipfile import ZipFile

working_dir_before = os.getcwd()
script_root = os.path.dirname(os.path.realpath(__file__))
working_dir_stack = list()
triplet = None

def chdir(path: str):
    os.chdir(path)
    print("Working dir:", os.getcwd())

def pushd(dir):
    working_dir_stack.append(os.getcwd())
    os.chdir(dir)
    print("Working dir:", os.getcwd())

def popd():
    os.chdir(working_dir_stack.pop())
    print("Working dir:", os.getcwd())

def run(command : str, env = os.environ):
    print("Execute:", command)
    subprocess.run(command, shell=True, env=env)

def remove_dir(dir : str):
    if os.path.isdir(str):
        shutil.rmtree(dir)

def download_file(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename} ...")
        urllib.request.urlretrieve(url, filename)
    print(f"Downloaded {filename}")

def extract_zip(filename, path="."):
    print(f"Extracting {filename} ...")
    with ZipFile(filename, "r") as zip:
        zip.extractall(path)
    print(f"Extracted {filename}")

def build_SDL():
    chdir(script_root + "/" + triplet)
    if not os.path.exists("SDL"):
        run("git clone https://github.com/libsdl-org/SDL.git")
    chdir("SDL")
    run("git pull")
    run("git checkout 8ec576ddabdc7edfd68e7a8a3214e84e4026328d")
    run("git submodule update --init --recursive")
    install_dir = os.getcwd() + "/installed"
    run(f"cmake -S . -B build -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX={install_dir}")
    run(f"cmake --build build --target install --config Release")

def build_SDL_mixer():
    chdir(script_root + "/" + triplet)
    if not os.path.exists("SDL_mixer"):
        run("git clone https://github.com/libsdl-org/SDL_mixer.git")
    chdir("SDL_mixer")
    run("git pull")
    run("git checkout 48701864697a904b3a771dcd20b5b6740f1c1d5c")
    run("git submodule update --init --recursive")
    install_dir = os.getcwd() + "/installed"
    sdl3_dir = script_root + f"/{triplet}/SDL/installed"
    run(f"cmake -S . -B build -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=\"{install_dir}\"",
                   env=dict(os.environ, SDL3_DIR=sdl3_dir))
    run(f"cmake --build build --target install --config Release")

def main() -> int:
    try:
        global triplet
        if platform.machine() == "AMD64":
            if platform.system() == "Windows":
                triplet = "x64-windows"
            if platform.system() == "Linux":
                triplet = "x64-linux"
        if platform is None:
            print("Cannot determine the target platform!")
            return 0
        if not os.path.exists(triplet):
            os.mkdir(triplet)

        print(f"Target Triplet: {triplet}")

        chdir(script_root)
        run("vcpkg install")
        build_SDL()
        build_SDL_mixer()

        chdir(script_root)
        if triplet == "x64-windows":
            chdir(triplet)
            download_file("https://dev.mysql.com/get/Downloads/Connector-C++/mysql-connector-c++-9.1.0-winx64.zip", "mysql-connector-c++-9.1.0-winx64.zip")
            extract_zip("mysql-connector-c++-9.1.0-winx64.zip")
        chdir(working_dir_before)
        return 0
    except Exception as e:
        print(e)
        chdir(working_dir_before)
        return -1

if __name__ == '__main__':
    sys.exit(main())
