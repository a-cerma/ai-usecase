<template>
    <main>
        <br/>
        <br/>
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
            <v-file-input
                v-model="video"
                width="1000"
                accept="video/mp4"
                label="File input"
                placeholder="Select your files"
                prepend-icon="mdi-file-video"
                variant="outlined"
                @change="handleFileUpload"
                counter
                
            >
        </v-file-input>
        <v-btn 
        :loading="isLoading"
        height="55" @click="uploadFile">Large Button</v-btn>
    
        </v-row>

        <v-row>
            <v-card color="#282828" style="border: 1px solid #007BFF;" width="auto">
                Color Palette for SmartLift

                ### 1. **Main Color for Logo and Highlighted Content**

                - **Electric Blue (#007BFF)**: dynamic and energetic feel that is perfect for a fitness app. Conveys trust, reliability, and a sense of cutting-edge technology.

                ### 2. **Background Color**

                - **Deep Gray (#282828) OR (#121212, darker)**: sleek and modern look, offering a softer alternative to pure black.

                ### 3. **Body Text Color**

                - **Soft White (#F5F5F5)**: excellent readability against the dark gray background. Less harsh than pure white.

                ### 4. **Accent Colors**

                - **Teal (#17A2B8)**: for secondary buttons and links, providing a harmonious match with the electric blue.

                OR

                - **Electric Orange (#FFA500)**: for calls to action and can energize the design, encouraging user interaction.

                - **Platinum (#E5E4E2)** or **Silver (#C0C0C0)**: for less prominent but necessary elements like secondary text or icons.
                Color Palette for SmartLift

                ### 1. **Main Color for Logo and Highlighted Content**

                - **Electric Blue (#007BFF)**: dynamic and energetic feel that is perfect for a fitness app. Conveys trust, reliability, and a sense of cutting-edge technology.

                ### 2. **Background Color**

                - **Deep Gray (#282828) OR (#121212, darker)**: sleek and modern look, offering a softer alternative to pure black.

                ### 3. **Body Text Color**

                - **Soft White (#F5F5F5)**: excellent readability against the dark gray background. Less harsh than pure white.

                ### 4. **Accent Colors**

                - **Teal (#17A2B8)**: for secondary buttons and links, providing a harmonious match with the electric blue.

                OR

                - **Electric Orange (#FFA500)**: for calls to action and can energize the design, encouraging user interaction.

                - **Platinum (#E5E4E2)** or **Silver (#C0C0C0)**: for less prominent but necessary elements like secondary text or icons.
            </v-card>
        </v-row>
    </main>

  </template>


<script setup>
import {ref} from 'vue'
import {launchExerciseAnalyzer} from '../api/launchExerciseAnalyzer'

const video = ref() 

const isLoading = ref(false)
const exerciseAnalysis = ref()

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
    console.log(response)
    exerciseAnalysis.value = JSON.parse(response)[0].review
    console.log('Exersise Analysis', JSON.parse(response)[0], response[0],response[0]["review"],exerciseAnalysis.value)
    isLoading.value = false

  }
  catch(error){
    console.error(error)
  }
  finally{
    isLoading.value = false
  }

}


</script>

<style scoped>
   .video{
    height: 200px!important;
    width: 300px!important;
   }
</style>