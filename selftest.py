"""Local tester for server.py and client.py - not the hidden grader.

    python3 selftest.py

Creates a files/ folder with two example files, starts your server.py in the background, and
downloads with your download_file. Change the examples and try your own.
"""
import os
import subprocess
import sys
import time

HOST = "127.0.0.1"
PORT = 2405


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    files = os.path.join(here, "files")
    os.makedirs(files, exist_ok=True)
    with open(os.path.join(files, "hello.txt"), "w") as f:
        f.write("meow\n")
    with open(os.path.join(files, "big.bin"), "wb") as f:
        f.write(bytes(range(256)) * 2000)

    server = subprocess.Popen([sys.executable, os.path.join(here, "server.py")], cwd=here)
    try:
        time.sleep(1)
        sys.path.insert(0, here)
        from client import download_file

        for name in ("hello.txt", "big.bin"):
            dest = os.path.join(here, "downloaded_" + name)
            if os.path.exists(dest):
                os.remove(dest)
            count = download_file(HOST, PORT, name, dest)
            if not os.path.exists(dest):
                print(name, "- returned", count, "- download_file did not save a file to dest")
                continue
            with open(os.path.join(files, name), "rb") as a, open(dest, "rb") as b:
                same = a.read() == b.read()
            print(name, "- returned", count, "- identical to the original:", same)
        print("missing file - returned", download_file(HOST, PORT, "nope.txt", os.path.join(here, "nope.txt")))
    finally:
        server.kill()


if __name__ == "__main__":
    main()
