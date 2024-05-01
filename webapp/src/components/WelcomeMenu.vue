<template>
  <MenuItem>
    <template #icon>
      <div class="header">
        <v-icon
          icon="mdi-weight-lifter"
          size="large"
        ></v-icon>
      </div>
    </template>
    <template #heading>
        <RouterLink to="/exercise-analyzer" :style="{fontWeight: 'bold'}">
          Exercise Analyzer 
        </RouterLink>
    </template>
    Perfect your form with SmartLift’s Exercise Analyzer. Upload a video of your workout and receive detailed feedback on your execution to maximize effectiveness and minimize injury.
  </MenuItem>

  <MenuItem>
    <template #icon>
      <v-icon
          icon="mdi-calendar-month"
          size="large"
        ></v-icon>
    </template>
    <template #heading>Workout Planner (Comming Soon)</template>
    Get a tailor-made fitness routine with the Workout Planner. Fill out a simple form about your fitness goals and preferences, and let SmartLift craft a personalized program just for you.
  </MenuItem>
  <MenuItem>
    <template #icon>
      <v-icon
          icon="mdi-robot-excited"
          size="large"
        ></v-icon>   
    </template>
    <template #heading>Virtual Coach (Comming Soon)</template>
    Interact with your Virtual Coach anytime. Ask questions, make adjustments to your workout plan, or seek fitness advice through an intuitive chat interface.
  </MenuItem>
  <MenuItem>
    <template #icon>
      <v-icon
          icon="mdi-finance"
          size="large"
        ></v-icon>
    </template>
    <template #heading>Progress Tracker (Comming Soon)</template>
    Visualize your fitness journey with the Progress Tracker. Upload photos of your physical evolution and receive an insightful analysis on your body’s changes and improvements.  </MenuItem>

  <MenuItem>
    <template #icon>
      <v-icon
          icon="mdi-noodles"
          size="large"
        ></v-icon>
    </template>
    <template #heading>Meal Scanner (Comming Soon)</template>
    Understand what you eat with the Meal Scanner. Snap a photo of your dish and get detailed nutritional information and feedback to align with your dietary goals.

  </MenuItem>

  <MenuItem>
    <template #icon>
      <v-icon
          icon="mdi-nutrition"
          size="large"
        ></v-icon>
    </template>
    <template #heading>Diet Designer (Comming Soon)</template>
    Create a personalized meal plan with the Diet Designer. Provide your dietary preferences and nutritional needs, and let SmartLift design a diet that supports your fitness journey.
  </MenuItem>
</template>
<script setup>
  import MenuItem from './MenuItem.vue'
  import { RouterLink } from 'vue-router'

</script>
<style scoped>
    .header{
      cursor: pointer;
    }
   
</style>
