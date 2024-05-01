from fastapi import APIRouter, HTTPException,  File, UploadFile
from fastapi.responses import JSONResponse
from ..services_to_be_reordered.frame_extraction import extract_frames_from_video
from ..services_to_be_reordered.video_analysis import analyze_video
# from ..models.video import Video

router = APIRouter()

@router.post("/exercise-analysis")
async def analyze_exercise_video(file: UploadFile = File(...)):
    try:
        video_bytes = await file.read()
        extract_frames_from_video(video_bytes, "frames")
        # Save file or process it here. For now, just return the file size.
        return analyze_video()
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})