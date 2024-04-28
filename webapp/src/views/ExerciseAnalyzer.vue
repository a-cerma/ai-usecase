<template>
    <br/>
    <br/>
    <v-file-input
        v-model="files"
        :show-size="1000"
        color="#008000"
        label="File input"
        placeholder="Select your files"
        prepend-icon="mdi-file-video"
        variant="outlined"
        counter
        multiple
  >
    <template v-slot:selection="{ fileNames }">
      <template v-for="(fileName, index) in fileNames" :key="fileName">
        <v-chip
          v-if="index < 2"
          class="me-2"
          color="#008000"
          size="small"
          label
        >
          {{ fileName }}
        </v-chip>

        <span
          v-else-if="index === 2"
          class="text-overline text-grey-darken-3 mx-2"
        >
          +{{ files.length - 2 }} File(s)
        </span>
      </template>
    </template>
  </v-file-input></template>

<script setup>
import {ref} from 'vue'

const files = ref([]) 

</script>

<style lang="scss" scoped>

</style>