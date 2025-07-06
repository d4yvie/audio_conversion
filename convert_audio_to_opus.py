import subprocess
import os
import time
from multiprocessing import Pool
from operator import is_not
from functools import partial
from contextlib import chdir
import sys


file_endings = ['.flac']
finished_marker = '.opus'


def convert_file(file: tuple[str, str]):
    root, name = file
    f = os.path.join(root, name)
    filename, file_extension = os.path.splitext(f)
    if (file_extension in file_endings) and not (finished_marker in f):
        print(f"converting {f}")
        subprocess.check_output(['opusenc', f, '--bitrate', '192', filename + '.opus' ])
        os.remove(f)
        return f
    return None


if __name__ == '__main__':
    """
    Converts the flac files of passed directory to opus.
    """
    start = time.time()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    args = sys.argv
    if len(args) > 2:
        os.chdir(args[1])
    print(f"Using directory: {os.getcwd()} recursively")
    files = [(root, f) for root, dirs, files in os.walk(".", topdown=True) for f in files]
    with Pool() as pool:
        result = list(pool.map(convert_file, files))
        converted_files = list(filter(partial(is_not, None), result))
        print("Done: converted following files:")
        print(converted_files)
        print(f"Converted {len(converted_files)} files")
    print(f"Conversion took {time.time() - start} seconds")
