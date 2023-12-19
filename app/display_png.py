import os
import time
from pathlib import Path
from shutil import copyfile

def main():

    detect_dir = Path("/detect")
    old_det_dir = detect_dir / "old"

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
    stream_frames_dir = frames_dir / "frames_stream"
    os.makedirs(stream_frames_dir, exist_ok=True)

    while not os.path.exists(stream_frames_dir):
        time.sleep(0.5)

    while True:
        
        try:
        
            for filename in sorted(os.listdir(frames_dir)):
                
                frame_count = len([filename for filename in os.listdir(stream_frames_dir)]) or 0
                copyfile(frames_dir / filename, stream_frames_dir / f"frame_{frame_count}.png")
                frame_count += 1
                
            time.sleep(0.5)
        
        except:
            
            print("no more frames to rename.")
                                    
if __name__ == "__main__":
    time.sleep(5)
    main()