<template>
    <div class="max-w-3xl mx-auto mt-10 p-8 bg-white rounded-lg shadow-lg">
      <h1 class="text-3xl font-bold text-center mb-8">Create Your Profile</h1>
  
      <form @submit.prevent="submitProfile" class="space-y-6">
        
        <div class="space-y-4">
          <Label>Description</Label>
          <Input v-model="form.description" placeholder="Enter description" />
        </div>
  
        <div class="space-y-4">
          <Label>Parish</Label>
          <Input v-model="form.parish" placeholder="Enter your parish" />
        </div>
  
        <div class="space-y-4">
          <Label>Biography</Label>
          <Textarea v-model="form.biography" placeholder="Tell us about yourself" />
        </div>
  
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <Label>Sex</Label>
            <Select v-model="form.sex">
              <option disabled value="">Select your sex</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </Select>
          </div>
  
          <div class="space-y-2">
            <Label>Race</Label>
            <Input v-model="form.race" placeholder="Enter your race" />
          </div>
        </div>
  
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <Label>Birth Year</Label>
            <Input v-model="form.birth_year" type="number" min="1900" max="2025" placeholder="Enter birth year" />
          </div>
  
          <div class="space-y-2">
            <Label>Height (inches)</Label>
            <Input v-model="form.height" type="number" step="0.1" placeholder="Enter your height" />
          </div>
        </div>
  
        <div class="grid grid-cols-2 gap-4">
          <div class="space-y-2">
            <Label>Favorite Cuisine</Label>
            <Input v-model="form.fav_cuisine" placeholder="Favorite cuisine" />
          </div>
  
          <div class="space-y-2">
            <Label>Favorite Colour</Label>
            <Input v-model="form.fav_colour" placeholder="Favorite color" />
          </div>
        </div>
  
        <div class="space-y-4">
          <Label>Favorite School Subject</Label>
          <Input v-model="form.fav_school_subject" placeholder="Favorite subject" />
        </div>
  
        <div class="flex flex-wrap gap-6 mt-6">
          <div class="flex items-center space-x-2">
            <Checkbox v-model="form.political" />
            <Label>Political</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Checkbox v-model="form.religious" />
            <Label>Religious</Label>
          </div>
          <div class="flex items-center space-x-2">
            <Checkbox v-model="form.family_oriented" />
            <Label>Family Oriented</Label>
          </div>
        </div>
  
        <Button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white mt-6">
          Submit Profile
        </Button>
  
        <div v-if="errorMessage" class="text-red-500 mt-4 text-center">
          {{ errorMessage }}
        </div>
  
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { createProfile } from '../services/api'; 
  
  const form = ref({
    description: '',
    parish: '',
    biography: '',
    sex: '',
    race: '',
    birth_year: '',
    height: '',
    fav_cuisine: '',
    fav_colour: '',
    fav_school_subject: '',
    political: false,
    religious: false,
    family_oriented: false,
  });
  
  const errorMessage = ref('');
  
  const submitProfile = async () => {
    try {
      await createProfile(form.value);
      alert('Profile created successfully!');
      //
    } catch (error) {
      console.error(error);
      errorMessage.value = 'Something went wrong while creating profile.';
    }
  }
  </script>
  