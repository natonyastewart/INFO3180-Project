<template>
    <div class="max-w-5xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-lg">
      <h1 class="text-3xl font-bold mb-6 text-center">My Profiles</h1>
  
            <div v-if="profiles.length" class="grid md:grid-cols-2 gap-6">
                <div
                        v-for="profile in profiles"
                        :key="profile.id"
                        @click="goToProfile(profile.id)"
                        class="cursor-pointer p-4 border rounded-lg shadow hover:shadow-lg transition bg-gray-50 hover:bg-white">
                                            <div class="flex items-center gap-4">
                                                <!-- Profile Image -->
                                                <img
                                                :src="profile.photo || 'https://via.placeholder.com/100'" 
                                                alt="Profile picture"
                                                class="w-20 h-20 rounded-full object-cover border"
                                                />
                                                <div>
                                                <h2 class="text-xl font-semibold">{{ profile.name }}</h2>
                                                <p class="text-gray-600 text-sm">{{ profile.description }}</p>
                                                </div>
                                            </div>
                                            <div class="mt-4 text-gray-700">
                                                <p><strong>Sex:</strong> {{ profile.sex }}</p>
                                                <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
                                                <p><strong>Height:</strong> {{ profile.height }} in</p>
                                                    </div>
                        </div>
                    </div>
        
            <div v-else class="text-center text-gray-500 mt-10">No profiles found.</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  // import { getUserProfiles } from '@/services/api' // Uncomment when api is ready !
  
  const router = useRouter()
  const profiles = ref([])
  
  
  const fetchProfiles = async () => {
    try {
      // const response = await getUserProfiles() // Uncomment when api is ready !
      // profiles.value = response.data            // Uncomment when api is ready !
    } catch (error) {
      console.error('Failed to fetch user profiles:', error)
    }
  }
 
  const goToProfile = (id) => {
    router.push({ name: 'ProfileDetails', params: { profile_id: id } })
  }
  
  onMounted(fetchProfiles)
  </script>
  