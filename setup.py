import os
import sys
import subprocess
import shutil
import asyncio
import aiohttp
from zipfile import ZipFile

working_dir_before_execute = os.getcwd()
script_root = os.path.dirname(os.path.realpath(__file__))
working_dir_stack = list()

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

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if "content-disposition" in response.headers:
                header = response.headers["content-disposition"]
                filename = header.split("filename=")[1]
            else:
                filename = url.split("/")[-1]
            print(f"Downloading {filename} from {url} ...")
            with open(filename, mode="wb") as file:
                while True:
                    chunk = await response.content.read()
                    if not chunk:
                        break
                    file.write(chunk)
            print(f"Downloaded {filename}")

def extract_zip(filename, path="."):
    with ZipFile(filename, "r") as zip:
        zip.extractall(path)

async def main() -> int:
    try:
        chdir(script_root)
        if not os.path.exists("x64-windows"):
            os.mkdir("x64-windows")
        chdir("x64-windows")
        urls = []
        if not os.path.exists("mysql-connector-c++-9.1.0-winx64.zip"):
            urls.append("https://dev.mysql.com/get/Downloads/Connector-C++/mysql-connector-c++-9.1.0-winx64.zip")
        downloads = [download_file(url) for url in urls]
        await asyncio.gather(*downloads)
        extract_zip("mysql-connector-c++-9.1.0-winx64.zip")
        chdir(working_dir_before_execute)
        return 0
    except Exception as e:
        print(e)
        chdir(working_dir_before_execute)
        return -1

if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
