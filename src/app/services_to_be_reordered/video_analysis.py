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
    frames: List[Frame], frame_range: Optional[tuple] = None
) -> List[Frame]:
    """Uploads frames specified by a range tuple (start, end) or all frames if no range is specified."""
    uploaded_files = []

    if frame_range is not None:
        start, end = frame_range
        # Correct the range if out of bounds
        start = max(0, start)
        end = min(len(frames), end)
        frames = frames[start:end]

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
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0,
        },
    )
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


def analyze_video():
    # Load environment and configure API
    env_path = pathlib.Path(__file__).parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    # Upload frames using the File API
    frames = list_frame_files(FRAME_EXTRACTION_DIRECTORY)
    frame_range = None  # Modify as needed
    # Uploads frames from index min to max-1
    # TODO: For now if some uploads fail we don't have a proper way to handle it and to clean up
    uploaded_files = upload_frames(frames, frame_range)

    # TODO: Can be deleted for speed
    # It was there to visually confirm the uploaded files
    list_uploaded_files(uploaded_files)

    # Generate content with the GenAI model
    prompt = """You are a fitness coach with expertise in biomechanics and injury prevention.
Analyze the given workout video. Identify the exercise performed and assess your coachee's execution. Provide feedback on their form and effectiveness to help improve their performance and prevent injury.
<ExpectedOutputFormat>
JSON format with 'exerciseName', 'review', and 'score' fields. Scores range from 1 to 10, with options for full or half
</ExpectedOutputFormat>
<Example>
{
    "exerciseName": "Weighted Pull-Ups",
    "review": "Your overall form is solid with good control during the ascent and descent. However, you are not fully extending your arms at the bottom of the movement, which can limit the range of motion and reduce the effectiveness of the exercise. Focus on full arm extension to engage the lats more completely and improve strength gains.",
    "score": 8.0
}
</Example>
<Example>
{
    "exerciseName": "Incline Barbell Bench Press",
    "review": "The angle of the bench and your grip width are appropriate for targeting the upper chest. Nonetheless, your elbows are flaring excessively, which can put undue stress on your shoulder joints. Aim to keep your elbows at a 45-degree angle relative to your torso to optimize muscle engagement and minimize injury risk.",
    "score": 6.5
}
</Example>"""
    model_name = "models/gemini-1.5-pro-latest"
    response = generate_content(uploaded_files, prompt, model_name)
    print(f"GenAI Answer:\n{response}\n")

    # Cleanup
    # TODO: Should be done asynchronously
    delete_uploaded_files(uploaded_files)
    return response


if __name__ == "__main__":
    analyze_video()
