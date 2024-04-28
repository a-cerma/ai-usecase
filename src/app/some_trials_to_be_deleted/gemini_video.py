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


def extract_frame_from_video(
    video_file_path: str, output_dir_path: str, output_file_prefix: str = "frame_"
) -> None:
    """Extracts frames from a video file at one frame per second."""
    print(f"Extracting frames from {video_file_path} at 1 frame per second...")

    create_replace_directory(output_dir_path)

    # Open the video file
    vidcap = cv2.VideoCapture(video_file_path)
    if not vidcap.isOpened():
        raise FileNotFoundError(f"Error: Could not open video file {video_file_path}.")

    try:
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))  # Number of frames per second
        fame_counter = 0
        while True:
            # Read the next frame
            success, frame = vidcap.read()
            if not success:  # End of video
                break

            # If the frame counter is a multiple of the frame rate, save the frame
            # If not, skip the frame but still increment the frame counter
            # This will extract one frame per second
            if fame_counter % fps == 0:
                time_string = (
                    f"{fame_counter // fps // 60:02d}:{fame_counter // fps % 60:02d}"
                )
                output_file_name = f"{output_file_prefix}{time_string}.jpg"
                output_file_path = os.path.join(output_dir_path, output_file_name)
                cv2.imwrite(output_file_path, frame)
                print(f"Extracted: {output_file_path}")

            fame_counter += 1
            print(
                f"Completed video frame extraction. Extracted {fame_counter // fps} frames."
            )
    finally:  # Ensure that the video capture object is always released
        vidcap.release()


if __name__ == "__main__":
    # TODO: change docstring
    """This script demonstrates how to use the Google GenAI API to generate content using the Gemini model."""

    video_file_name = "https://storage.googleapis.com/generativeai-downloads/data/SherlockJr._10min.mp4"

    extract_frame_from_video(video_file_name, "frames")

    # Traverse up two directories
    # env_path = pathlib.Path(__file__).parents[2] / ".env"
    # load_dotenv(dotenv_path=env_path)

    # genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    # response = model.generate_content("Please give me python code to sort a list.")
    # print(response.text)
