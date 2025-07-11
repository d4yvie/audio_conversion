import subprocess
import os
import time
import sys
from multiprocessing import Pool
from operator import is_not
from functools import partial


file_endings = ['.flac']
finished_marker = '.opus'


def convert_file(file: tuple[str, str]) -> str | None:
    try:
        root, name = file
        f = os.path.join(root, name)
        filename, file_extension = os.path.splitext(f)
        if (file_extension in file_endings) and not (finished_marker in f):
            print(f"converting {f}")
            subprocess.check_output(['opusenc', f, '--bitrate', '192', filename + '.opus' ])
            os.remove(f)
            return f
    except Exception as e:
        print(f"failed to convert file: {e}")
    return None


def du(path: str) -> str:
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')


if __name__ == '__main__':
    """
    Converts the flac files of passed directory to opus.
    """
    start = time.time()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    args = sys.argv
    if len(args) > 1:
        os.chdir(args[1])
    print(f"Using directory: {os.getcwd()} recursively")
    du_before = du('.');
    files = [(root, f) for root, dirs, files in os.walk(".", topdown=True) for f in files]
    with Pool() as pool:
        result = list(pool.map(convert_file, files))
        converted_files = list(filter(partial(is_not, None), result))
        print("Done: converted following files:")
        print(converted_files)
        print(f"Converted {len(converted_files)} files")
    print(f"Conversion took {time.time() - start} seconds")
    print(f"du before: {du_before}, du after: {du('.')}")
