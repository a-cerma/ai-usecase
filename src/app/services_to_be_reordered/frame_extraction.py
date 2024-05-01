import os
import shutil
import numpy as np
import tempfile
import cv2


def create_or_replace_directory(dir_path: str) -> None:
    """Creates a directory or replaces it if it already exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

def extract_frames_from_video(video_bytes: bytes, output_dir_path: str) -> None:
    """Extracts one frame per second from video bytes and saves it as a JPEG image in the output directory."""
    create_or_replace_directory(output_dir_path)

    # Create a temporary file to store video bytes
    temp_video_file_path = None  # Declare outside the with statement to extend its scope
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            temp_video_file.write(video_bytes)
            temp_video_file.flush()  # Ensure all data is written to disk
            temp_video_file_path = temp_video_file.name

        video_capture = cv2.VideoCapture(temp_video_file_path)
        if not video_capture.isOpened():
            raise FileNotFoundError("Could not open video data")

        fps = round(video_capture.get(cv2.CAP_PROP_FPS))  # Number of frames per second
        frame_counter = 0
        nb_frames_extracted = 0
        output_file_prefix = "extracted_frame_"

        while True:
            # Read the next frame
            success, frame = video_capture.read()
            if not success:  # End of video
                break

            if frame_counter % fps == 0:  # Extract a frame every second
                min = nb_frames_extracted // 60
                sec = nb_frames_extracted % 60
                time_string = f"{min:02d}-{sec:02d}"  # Format the time as MM-SS
                output_file_name = f"{output_file_prefix}{time_string}.jpg"
                output_file_path = os.path.join(output_dir_path, output_file_name)
                cv2.imwrite(output_file_path, frame)
                print(f"Extracted: {output_file_path}")
                nb_frames_extracted += 1

            frame_counter += 1
        print(
            f"Completed video frame extraction. Extracted {nb_frames_extracted} frames."
        )
    finally:  # Ensure that the video capture object and temporary file are always released
        if video_capture:
            video_capture.release()
        if temp_video_file_path:
            os.unlink(temp_video_file_path)  # Delete the temporary file

if __name__ == "__main__":
    video_file_path = "videos/kickback.mp4"

    extract_frames_from_video(video_file_path, "frames")
