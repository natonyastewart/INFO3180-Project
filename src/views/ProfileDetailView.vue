<template>
    <div class="max-w-3xl mx-auto mt-10 p-8 bg-white rounded-xl shadow-xl border border-gray-200">
      <h1 class="text-3xl font-semibold text-center text-gray-800 mb-6">Profile Details</h1>
  
      <div v-if="profile" class="space-y-6">
        
                    <!-- Profile Image -->
                    <div class="flex justify-center">
                    <img
                        :src="profile.photo || 'https://via.placeholder.com/150'"
                        alt="Profile Picture"
                        class="w-40 h-40 object-cover rounded-full border-4 border-gray-200 shadow-md"
                    />
                    </div>
  
                            <!-- Profile Info -->
                            <div class="space-y-4 text-gray-700">
                            <p><strong class="font-semibold">Name:</strong> {{ profile.name }}</p>
                            <p><strong class="font-semibold">Sex:</strong> {{ profile.sex }}</p>
                            <p><strong class="font-semibold">Race:</strong> {{ profile.race }}</p>
                            <p><strong class="font-semibold">Parish:</strong> {{ profile.parish }}</p>
                            <p><strong class="font-semibold">Birth Year:</strong> {{ profile.birth_year }}</p>
                            <p><strong class="font-semibold">Height:</strong> {{ profile.height }} inches</p>
                            <p><strong class="font-semibold">Favorite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
                            <p><strong class="font-semibold">Favorite Colour:</strong> {{ profile.fav_colour }}</p>
                            <p><strong class="font-semibold">Favorite School Subject:</strong> {{ profile.fav_school_subject }}</p>
                            <p><strong class="font-semibold">Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
                            <p><strong class="font-semibold">Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
                            <p><strong class="font-semibold">Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
                            <p><strong class="font-semibold">Biography:</strong> {{ profile.biography }}</p>
                            </div>
  
                            <!-- Action Buttons Section -->
                            <div class="flex justify-center gap-8 mt-6">
                            <button
                                @click="toggleFavourite"
                                :class="[
                                'px-6 py-3 rounded-lg font-semibold text-lg flex items-center transition duration-300',
                                isFavourited ? 'bg-red-600 text-white' : 'bg-gray-200 text-black hover:bg-red-100'
                                ]"
                            >
                                <span class="mr-3 text-2xl">❤️</span>
                                {{ isFavourited ? 'Favourited' : 'Add to Favourites' }}
                            </button>
                    
                            <button
                                class="bg-gray-300 hover:bg-gray-400 text-black px-6 py-3 rounded-lg font-semibold text-lg"
                            >
                                📧 Email Profile
                            </button>
                            </div>
  
                            <!-- Message Section -->
                            <div v-if="message" class="text-green-600 mt-4 text-center font-semibold">
                            {{ message }}
                            </div>
                        </div>
  
      <div v-else class="text-gray-600 text-center">Loading profile...</div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';

  // import { getProfileById, addToFavorites } from '@/services/api'; //uncomment when api is ready !
  
  const route = useRoute();
  const profileId = route.params.profile_id as string;
  const profile = ref(null);
  const message = ref('');
  const isFavourited = ref(false);
  
  const toggleFavourite = async () => {
    try {

      // await addToFavorites(profile.value.id); //uncomment when api is ready !
      isFavourited.value = !isFavourited.value;
      message.value = isFavourited.value ? 'Profile added to your favourites!' : '';
    } catch (error) {
      console.error('Failed to favourite profile:', error);
      message.value = 'Something went wrong.';
    }
  };
  
  // Fetch profile data when the component is mounted (real API call should go here)
  onMounted(() => {
    // fetchProfile(profileId); //uncomment and replace with correct api stuff !
  
    // const fetchedProfile = await getProfileById(profileId); //uncomment and replace with correct api stuff !
    // profile.value = fetchedProfile; //uncomment and replace with correct api stuff !
  });
  </script>
  
  <style scoped>
  body {
    font-family: 'Inter', sans-serif;
  }
  
  h1 {
    font-family: 'Helvetica Neue', sans-serif;
  }
  
  button {
    transition: all 0.3s ease-in-out;
  }
  
  button:hover {
    transform: scale(1.05);
  }
  
  button:focus {
    outline: none;
  }
  
  /* spacing and font sizes */
  p {
    font-size: 16px;
    line-height: 1.5;
  }
  
  strong {
    font-weight: bold;
  }
  </style>
  