<template>
  <div class="max-w-3xl mx-auto mt-10 p-8 bg-white rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold text-center mb-8">Create Your Profile</h1>

              <form @submit.prevent="submitProfile" class="space-y-6">

                        <!-- Profile Image Upload -->
                        <div class="space-y-2">
                          <label class="block font-medium">Profile Picture</label>
                          <input type="file" @change="handleFileUpload" accept="image/*" />
                        </div>

                        <!-- Description -->
                        <div class="space-y-2">
                          <label class="block font-medium">Description</label>
                          <input v-model="form.description" class="w-full border rounded p-2" placeholder="Enter description" />
                        </div>

                        <!-- Parish -->
                        <div class="space-y-2">
                          <label class="block font-medium">Parish</label>
                          <input v-model="form.parish" class="w-full border rounded p-2" placeholder="Enter parish" />
                        </div>

                        <!-- Biography -->
                        <div class="space-y-2">
                          <label class="block font-medium">Biography</label>
                          <textarea v-model="form.biography" class="w-full border rounded p-2" placeholder="Tell us about yourself" />
                        </div>

                        <!-- Sex & Race -->
                        <div class="grid grid-cols-2 gap-4">
                          <div class="space-y-2">
                            <label class="block font-medium">Sex</label>
                            <select v-model="form.sex" class="w-full border rounded p-2">
                              <option disabled value="">Select your sex</option>
                              <option>Male</option>
                              <option>Female</option>
                              <option>Non-Binary</option>
                              <option>Prefer Not To Say</option>
                              <option>Other</option>
                            </select>
                          </div>

                          <div class="space-y-2">
                            <label class="block font-medium">Race</label>
                            <input v-model="form.race" class="w-full border rounded p-2" placeholder="Enter race" />
                          </div>
                        </div>

                        <!-- Birth Year & Height -->
                        <div class="grid grid-cols-2 gap-4">
                          <div class="space-y-2">
                            <label class="block font-medium">Birth Year</label>
                            <input v-model="form.birth_year" type="number" min="1900" max="2025" class="w-full border rounded p-2" />
                          </div>

                          <div class="space-y-2">
                            <label class="block font-medium">Height (inches)</label>
                            <input v-model="form.height" type="number" step="0.1" class="w-full border rounded p-2" />
                          </div>
                        </div>

                        <!-- Cuisine & Colour -->
                        <div class="grid grid-cols-2 gap-4">
                          <div class="space-y-2">
                            <label class="block font-medium">Favorite Cuisine</label>
                            <input v-model="form.fav_cuisine" class="w-full border rounded p-2" />
                          </div>

                          <div class="space-y-2">
                            <label class="block font-medium">Favorite Colour</label>
                            <input v-model="form.fav_colour" class="w-full border rounded p-2" />
                          </div>
                        </div>

                        <!-- Favorite School Subject -->
                        <div class="space-y-2">
                          <label class="block font-medium">Favorite School Subject</label>
                          <input v-model="form.fav_school_subject" class="w-full border rounded p-2" />
                        </div>

                        <!-- Checkboxes -->
                        <div class="flex flex-wrap gap-6 mt-6">
                          <label class="flex items-center space-x-2">
                            <input type="checkbox" v-model="form.political" />
                            <span>Political</span>
                          </label>
                          <label class="flex items-center space-x-2">
                            <input type="checkbox" v-model="form.religious" />
                            <span>Religious</span>
                          </label>
                          <label class="flex items-center space-x-2">
                            <input type="checkbox" v-model="form.family_oriented" />
                            <span>Family Oriented</span>
                          </label>
                        </div>

                        <!-- Submit Button -->
                        <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded">
                          Submit Profile
                        </button>

                        <!-- Error Message -->
                        <div v-if="errorMessage" class="text-red-500 mt-4 text-center">
                          {{ errorMessage }}
                        </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createProfile } from '../services/api'

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
})

const selectedFile = ref(null)
const errorMessage = ref('')

const handleFileUpload = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    selectedFile.value = file
  }
}

const submitProfile = async () => {
  try {
    const formData = new FormData()
    for (const key in form.value) {
      formData.append(key, form.value[key])
    }

    if (selectedFile.value) {
      formData.append('photo', selectedFile.value)
    }

    // backend FormData
    await createProfile(formData)

    alert('Profile created successfully!')
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Something went wrong while creating your profile.'
  }
}
</script>
