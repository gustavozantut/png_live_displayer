import os
import re
import time
import subprocess
from pathlib import Path
from shutil import copyfile

def execute_gst_command(file_path):
    command = [
        "/bin/bash",
        "-c",
        f"gst-launch-1.0 -v filesrc location=\"{file_path}\" ! decodebin ! videoconvert ! imagefreeze num-buffers=10 ! autovideosink"
    ]
    subprocess.run(command)
    
def replace_log_filenames(input_string):
    pattern = re.compile(r'_[0-9]+\.log')
    output_string = re.sub(pattern, '.png', input_string)
    return output_string

def main():

    detect_dir = Path("/detect")
    old_det_dir = detect_dir / "old"
    logs_dir = Path("/logs")

    while not [
        item
        for item in detect_dir.glob("*")
        if not os.path.samefile(item, old_det_dir)
        and not os.path.commonpath([item, old_det_dir]) == old_det_dir
    ]:
        time.sleep(0.5)

    latest_detection = sorted(
        [item
         for item in detect_dir.glob("*")
         if not os.path.samefile(item, old_det_dir)
         and not os.path.commonpath([item, old_det_dir]) == old_det_dir
         ],
        key=lambda x: x.stat().st_mtime,
        reverse=True,
    )[0].name

    frames_dir = detect_dir / latest_detection / "frames"
    frames_with_plates_det_dir = frames_dir / "plates_displayed"
    os.makedirs(frames_with_plates_det_dir, exist_ok=True)

    while not os.path.exists(frames_with_plates_det_dir):
        time.sleep(0.5)

    while True:
        
        try:
        
            for folder_name, subfolders, files in os.walk(logs_dir / latest_detection / "posted_plates"):
                
                for filename in sorted(files):
                    
                    filename = replace_log_filenames(filename)
                    
                    if filename not in os.listdir(frames_with_plates_det_dir):
                    
                        file_path = os.path.join(frames_dir, filename)
                        execute_gst_command(file_path)
                        copyfile(frames_dir / filename, frames_with_plates_det_dir / f"{filename}")
                
            time.sleep(1)
        
        except:
            
            print("no more frames to rename.")
                                    
if __name__ == "__main__":
    time.sleep(5)
    main()