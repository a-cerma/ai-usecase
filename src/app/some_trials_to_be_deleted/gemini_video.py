import os
import shutil

import cv2


def create_or_replace_directory(dir_path: str) -> None:
    """Creates a directory or replaces it if it already exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def extract_frames_from_video(video_file_uri: str, output_dir_path: str) -> None:
    """Extracts one frame per second from a video file and saves it as a JPEG image in the output directory."""
    create_or_replace_directory(output_dir_path)

    video_capture = cv2.VideoCapture(video_file_uri)
    if not video_capture.isOpened():
        raise FileNotFoundError(f"Could not open video file: {video_file_uri}")

    fps = round(video_capture.get(cv2.CAP_PROP_FPS))  # Number of frames per second
    frame_counter = 0
    nb_frames_extracted = 0
    output_file_prefix = os.path.basename(video_file_uri).replace(".", "_")
    output_file_prefix += "_frame_"

    try:
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
    finally:  # Ensure that the video capture object is always released
        video_capture.release()


if __name__ == "__main__":
    video_file_uri = "https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4"

    extract_frames_from_video(video_file_uri, "frames")
