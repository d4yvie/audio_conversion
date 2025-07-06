import subprocess
import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]
file_endings = ['.mkv', 'mp4']
finished_marker = 'converted_'

for f in files:
    filename, file_extension = os.path.splitext(f)
    if (file_extension in file_endings) and not (finished_marker in filename):
        subprocess.check_output(['ffmpeg', '-i', f, '-c:v', 'copy', '-c:a', 'libopus', '-b:a', '320k', finished_marker + f ])
