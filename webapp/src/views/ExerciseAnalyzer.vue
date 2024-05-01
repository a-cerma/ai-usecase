<template>
    <main>
        <v-row>
            <v-responsive>
                <video ref="videoPlayer" width="auto" height="350" v-if="video" controls>
                    <!-- <source :src="videoSrc"   style="max-width: 100%;" class="video" type="video/mp4" > -->
                    Your browser does not support the video tag.
                </video>
            </v-responsive>
        </v-row>
        <br/>
        <br/>
        <v-row>
            <v-col>
                <v-file-input
                    v-model="video"
                    width="1000"
                    accept="video/mp4"
                    label="File input"
                    placeholder="Select your files"
                    prepend-icon="mdi-file-video"
                    variant="outlined"
                    :style="{cursor:'pointer'}"
                    @change="handleFileUpload"
                    counter
                    
                >
                </v-file-input>
            </v-col>
            <v-col>
              <v-btn 
                  cols="auto" 
                  size="x-large" 
                  prepend-icon="mdi-play" 
                  class="custom-btn"  
                  color="#007BFF" 
                  :ripple="false"
                  :loading="isLoading"
                  @click="uploadFile" 
                >Start Analysis</v-btn>
            </v-col>
    
        </v-row>
        <br/>
        <br/>
        <v-row  v-if="exerciseAnalysisResult" >
              <div class="title"> Exercise Detected: </div> {{ exerciseAnalysisResult.exerciseName }}
        </v-row>
        <v-row v-if="exerciseAnalysisResult" >
            <div class="title">Rating: </div> <div :style="{color:getScoreColor(exerciseAnalysisResult.score), fontWeight: 'bold'}"> {{ exerciseAnalysisResult.score }}/10</div>
        </v-row>
        <br>
        <br>
        <v-row   v-if="exerciseAnalysisResult">
            {{ exerciseAnalysisResult.review }} 
        </v-row>
        
    </main>

  </template>


<script setup>
import {ref} from 'vue'
import {launchExerciseAnalyzer} from '../api/launchExerciseAnalyzer'

const video = ref() 

const isLoading = ref(false)
const exerciseAnalysisResult = ref()

const videoPlayer = ref(null);

function handleFileUpload(event) {
  const files = event.target.files;
  if (files.length > 0) {
    video.value = files[0]; // The first selected file
    const reader = new FileReader();

    reader.onload = (event) => {
          videoPlayer.value.src = event.target.result;
     };

    reader.readAsDataURL(video.value);
  }




}

const uploadFile=async()=>{
  if (!video.value) return;


  const formData = new FormData();
  formData.append('file', video.value);
  
  try{
    isLoading.value = true
    const response = await launchExerciseAnalyzer(formData)
    exerciseAnalysisResult.value = JSON.parse(response)[0]
    isLoading.value = false

  }
  catch(error){
    console.error(error)
  }
  finally{
    isLoading.value = false
  }

}

const getScoreColor = (score)=>{
    if(score > 0 && score <= 4){
         return '#FF0000'
    }
    else if(score > 4 && score <7){
         return '#FFA500'
    }
    else if(score>=6 && score<=10){
         return '#008000'
    }
}
</script>

<style scoped>
   .video{
    height: 200px!important;
    width: 300px!important;
   }
   .title {
    /* font-size: 1.2rem; */
    /* font-weight: 500; */
    /* margin-bottom: 0.4rem; */
    font-weight: bold;
    color: var(--color-heading);
    padding-right: 7px;
    }
    .custom-btn:hover {
        /* Reset hover styles to default */
        background-color: inherit !important;
        color: inherit !important;
        cursor: pointer;

        }

</style>