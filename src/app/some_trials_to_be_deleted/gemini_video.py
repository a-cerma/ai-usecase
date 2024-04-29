import os
import pathlib
from typing import List, Optional

import google.generativeai as genai
from dotenv import load_dotenv

FRAME_PREFIX = "_frame_"
FRAME_EXTRACTION_DIRECTORY = "frames"


class Frame:
    """Represents a frame file with associated metadata and operations."""

    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.timestamp: str = self._extract_timestamp(file_path)
        self.display_name = None  # TODO: Check if this is needed
        self.response = None  # TODO: Find the type

    def _extract_timestamp(self, filename: str) -> str:
        """Extracts the timestamp from the filename, assuming the format '***_frame_MM-SS.jpg'."""
        parts = filename.split(FRAME_PREFIX)
        if len(parts) != 2:
            raise ValueError(f"Filename format is incorrect: {filename}")
        # NB: A dash was needed in the filename because colons are not allowed in filenames
        timestamp_with_dash = parts[1].split(".")[0]
        timestamp_with_colon = timestamp_with_dash.replace("-", ":")
        return timestamp_with_colon

    def upload(self):
        """Uploads the frame file and stores the response."""
        print(f"Uploading {self.file_path}")
        self.response = genai.upload_file(path=self.file_path)


def list_frame_files(directory: str) -> List[Frame]:
    """Lists sorted frame files in the specified directory."""
    files = sorted(os.listdir(directory))
    return [Frame(os.path.join(directory, file)) for file in files]


def upload_frames(
    frames: List[Frame], nb_frames_to_upload: Optional[int] = None
) -> List[Frame]:
    """Uploads a specified number of frames or all frames if no limit is specified."""
    uploaded_files = []
    # TODO: Change with a slice instead of taking the first n frames
    if nb_frames_to_upload is not None and nb_frames_to_upload < len(frames):
        frames = frames[:nb_frames_to_upload]
    print(f"Uploading {len(frames)} files...")
    for frame in frames:
        frame.upload()
        uploaded_files.append(frame)
    print(f"Upload completed!\n")
    return uploaded_files


def list_uploaded_files(uploaded_files: List[Frame]):
    """Prints URIs of all uploaded frames."""
    print("List of all uploaded files:")
    for file in uploaded_files:
        print(file.response.uri)
    print()  # Newline


def generate_content(files: List[Frame], prompt: str, model_name: str) -> str:
    """Generates content based on uploaded frames using a specified model."""
    model = genai.GenerativeModel(model_name=model_name)
    request = [prompt]
    for file in files:
        request.append(file.timestamp)
        request.append(file.response)

    response = model.generate_content(request, request_options={"timeout": 600})
    return response.text


def delete_uploaded_files(files: List[Frame]):
    """Deletes uploaded frames from the server."""
    print(f"Deleting {len(files)} files...")
    for file in files:
        genai.delete_file(file.response.name)
        print(f"Deleted {file.file_path} at URI {file.response.uri}")
    print(f"Deletion completed!")


def main():
    # Load environment and configure API
    env_path = pathlib.Path(__file__).parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Upload frames using the File API
    frames = list_frame_files(FRAME_EXTRACTION_DIRECTORY)
    nb_frames_to_upload = 2  # Modify as needed
    uploaded_files = upload_frames(frames, nb_frames_to_upload)

    list_uploaded_files(uploaded_files)

    # Generate content with the GenAI model
    prompt = "Describe this video."
    model_name = "models/gemini-1.5-pro-latest"
    response = generate_content(uploaded_files, prompt, model_name)
    print(f"GenAI Answer:\n{response}\n")

    # Cleanup
    delete_uploaded_files(uploaded_files)


if __name__ == "__main__":
    main()
