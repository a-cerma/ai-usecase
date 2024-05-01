import axios from "axios";

export const launchExerciseAnalyzer = async (encodedVideo) => {
  const apiUrl = import.meta.env.VITE_BACKEND_URL + '/exercise-analysis';

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