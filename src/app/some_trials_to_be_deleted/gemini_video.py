import os
import pathlib
import shutil

import cv2
import google.generativeai as genai
from dotenv import load_dotenv


def create_replace_directory(dir_path: str) -> None:
    """Creates a directory if it does not exist. If it exists, it is deleted and recreated."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path)
        os.makedirs(dir_path)


def extract_frame_from_video(video_file_uri: str, output_dir_path: str) -> None:
    """Extracts one frame per second from a video file and saves it as a JPEG image."""
    create_replace_directory(output_dir_path)

    video_capture = cv2.VideoCapture(video_file_uri)

    fps = int(video_capture.get(cv2.CAP_PROP_FPS))  # Number of frames per second
    frame_counter = 0
    nb_frames_extracted = 0
    output_file_prefix = os.path.basename(video_file_uri).replace(".", "_")
    output_file_prefix += "_frame_"

    try:
        while video_capture.isOpened():
            # Read the next frame
            success, frame = video_capture.read()
            if not success:  # End of video
                break

            # If the frame counter is a multiple of the frame rate, save the frame
            # Otherwise, skip the frame but still increment the frame counter
            # This will extract one frame per second
            if frame_counter % fps == 0:
                time_string = (
                    f"{frame_counter // fps // 60:02d}-{frame_counter // fps % 60:02d}"
                )
                output_file_name = f"{output_file_prefix}{time_string}.jpg"
                output_file_path = os.path.join(output_dir_path, output_file_name)
                cv2.imwrite(output_file_path, frame)
                print(f"Extracted: {output_file_path}")
                nb_frames_extracted += 1

            frame_counter += 1
        print(
            f"Completed video frame extraction. Extracted {nb_frames_extracted} frames."
        )
    finally:  # Ensure that the video capture object is always released
        video_capture.release()


if __name__ == "__main__":
    video_file_uri = "https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4"

    extract_frame_from_video(video_file_uri, "frames")
