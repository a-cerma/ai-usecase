import axios from "axios";

export const launchExerciseAnalyzer = async (encodedVideo) => {
  const apiUrl = 'http://127.0.0.1:8000/exercise-analysis';

  return axios.post(apiUrl, encodedVideo, {
    headers: {
      'Content-Type': 'multipart/form-data',
    }
  })
  .then(response => {
    console.log('Data submitted successfully:', response.data);
    return response.data;
  })
  .catch(error => {
    console.error('Error submitting data:', error);
    throw error;  // Ensure that the error is re-thrown so it can be caught by the calling function
  });
};