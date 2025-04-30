<template>
    <div class="max-w-5xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-lg">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-8">Your Favourite Profiles</h1>
  
      <div v-if="favourites.length" class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        <div
                    v-for="profile in favourites"
                    :key="profile.id"
                    class="bg-gray-50 border border-gray-200 p-4 rounded-lg shadow hover:shadow-md transition">
          
                <img
                    :src="profile.photo || 'https://via.placeholder.com/150'"
                    alt="Profile Picture"
                    class="w-full h-48 object-cover rounded-md mb-4"/>

                        <h2 class="text-xl font-semibold mb-2">{{ profile.name }}</h2>
                        <p class="text-sm text-gray-600 mb-1"><strong>Sex:</strong> {{ profile.sex }}</p>
                        <p class="text-sm text-gray-600 mb-1"><strong>Race:</strong> {{ profile.race }}</p>
                        <p class="text-sm text-gray-600 mb-1"><strong>Parish:</strong> {{ profile.parish }}</p>
  
                                <router-link
                                    :to="`/profiles/${profile.id}`"
                                    class="inline-block mt-4 text-blue-600 hover:underline font-medium">
                                    View More Details →
                                </router-link>
                                </div>
                            </div>
  
                                <div v-else class="text-center text-gray-500 text-lg">
                                    No favourites found.
                                </div>
                                </div>
                            </template>
                            
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  // import { getFavourites } from '@/services/api' // Uncomment when api is ready !!!
  import type { Profile } from '@/services/api.types'
  
  const favourites = ref<Profile[]>([])
  
  const fetchFavourites = async () => {
    try {
      // favourites.value = await getFavourites() // uncomment and replace with api stuff !!!
    } catch (error) {
      console.error('Failed to load favourites:', error)
    }
  }
  
  onMounted(fetchFavourites)
  </script>
  