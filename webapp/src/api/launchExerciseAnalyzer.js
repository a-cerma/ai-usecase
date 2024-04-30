import axios from "axios";
export const launchExerciseAnalyzer = async(encodedVideo)=>{
    const apiUrl = 'http://127.0.0.1:8000/exercise-analysis';
    //TODO put as input of the function

    axios.post(apiUrl, encodedVideo, {
        headers: {
          'Content-Type': 'multipart/form-data', // Specify that you'rmultipart/form-datae sending binary data
        }
      })
    .then(response => {
        console.log('Data submitted successfully:', response.data);
        return response.data
    })
    .catch(error => {
      console.error('Error submitting data:', error);
    });
}