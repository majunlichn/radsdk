import os
import sys
import platform
import subprocess
import shutil
import urllib.request
from zipfile import ZipFile

working_dir_before_execute = os.getcwd()
script_root = os.path.dirname(os.path.realpath(__file__))
working_dir_stack = list()
platform_name = None

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
    with ZipFile(filename, "r") as zip:
        zip.extractall(path)

def build_SDL():
    print(f"Build Platform: {platform_name}")
    chdir(script_root + "/" + platform_name)
    if not os.path.exists("SDL"):
        run("git clone https://github.com/libsdl-org/SDL.git --depth=1")
    chdir("SDL")
    run("git checkout 5608bf5866ee2b6749990f0e2b70026c0e43b3e5")
    run("git submodule update --init --recursive")
    install_dir = os.getcwd() + "/installed"
    run(f"cmake -S . -B build -D CMAKE_INSTALL_PREFIX={install_dir}")
    run(f"cmake --build build --target install --config Release")

def build_SDL_mixer():
    chdir(script_root + "/" + platform_name)
    if not os.path.exists("SDL_mixer"):
        run("git clone https://github.com/libsdl-org/SDL_mixer.git --depth=1")
    chdir("SDL_mixer")
    run("git checkout 90859376266adcd602499e94e0ac0c10fb55f712")
    run("git submodule update --init --recursive")
    install_dir = os.getcwd() + "/installed"
    sdl3_dir = script_root + f"/{platform_name}/SDL/installed"
    run(f"cmake -S . -B build -D CMAKE_INSTALL_PREFIX=\"{install_dir}\"",
                   env=dict(os.environ, SDL3_DIR=sdl3_dir))
    run(f"cmake --build build --target install --config Release")

def main() -> int:
    try:
        global platform_name
        if platform.machine() == "AMD64":
            if platform.system() == "Windows":
                platform_name = "x64-windows"
            if platform.system() == "Linux":
                platform_name = "x64-linux"
        if platform is None:
            print("Cannot determine the target platform!")
            return 0
        if not os.path.exists(platform_name):
            os.mkdir(platform_name)

        print(f"Build Platform: {platform_name}")

        chdir(script_root)
        build_SDL()
        build_SDL_mixer()

        chdir(script_root)
        chdir(platform_name)
        download_file("https://dev.mysql.com/get/Downloads/Connector-C++/mysql-connector-c++-9.1.0-winx64.zip", "mysql-connector-c++-9.1.0-winx64.zip")
        extract_zip("mysql-connector-c++-9.1.0-winx64.zip")
        chdir(working_dir_before_execute)
        return 0
    except Exception as e:
        print(e)
        chdir(working_dir_before_execute)
        return -1

if __name__ == '__main__':
    sys.exit(main())
