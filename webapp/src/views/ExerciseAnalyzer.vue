<template>
    <main>
        <br/>
        <br/>

        <v-row>
            <v-file-input
                v-model="file"
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
            <v-card color="#181818" style="border: 1px solid #008000;" width="800">
                {{ exerciseAnalysis }}
            </v-card>
        </v-row>
    </main>

  </template>


<script setup>
import {ref} from 'vue'
import {launchExerciseAnalyzer} from '../api/launchExerciseAnalyzer'

const file = ref([]) 
const isLoading = ref(false)
const exerciseAnalysis = ref()

function handleFileUpload(event) {
  const files = event.target.files;
  if (files.length > 0) {
    file.value = files[0]; // The first selected file
  }
}

const uploadFile=async()=>{
  if (!file.value) return;


  const formData = new FormData();
  console.log([...formData])
  formData.append('file', file.value);
  try{
    isLoading.value = true
    console.log('is loading',formData,  isLoading.value)
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

<style lang="scss" scoped>

</style>