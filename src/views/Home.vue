<script setup lang="ts">
import type { Profile, ProfileSearchParams } from '../services/api.types';
import type { UserData } from '../store';

import axios from 'axios';
import { onMounted, ref } from 'vue';
import ProfileCard from '../components/ProfileCard.vue';
import SearchForm from '../components/SearchForm.vue';
import { getAllProfiles, getUserFavorites, searchProfiles } from '../services/api';
import { getCurrentUser } from '../services/auth';

// Define reactive state
const profiles = ref<Profile[]>([]);
const favorites = ref<string[]>([]);
const loading = ref<boolean>(true);
const isSearching = ref<boolean>(false);
const hasProfiles = ref<boolean>(false);
const currentUser = ref<UserData | null>(null);

// Initialize data
onMounted(async () => {
	currentUser.value = getCurrentUser();
	await checkUserProfile();

	if (hasProfiles.value) {
		await Promise.all([loadProfiles(), loadFavorites()]);
	}
});

// Check if user has a profile
const checkUserProfile = async (): Promise<void> => {
	try {
		if (currentUser.value?.id) {
			// Check if user has at least one profile
			const response = await axios.get(`/api/users/${currentUser.value.id}`);
			hasProfiles.value = response.data.profiles && response.data.profiles.length > 0;
		}
	} catch (error) {
		console.error('Error checking user profile:', error);
		hasProfiles.value = false;
	}
};

// Load profiles
const loadProfiles = async (): Promise<void> => {
	loading.value = true;
	try {
		const data = await getAllProfiles();
		// Filter out current user's profiles
		if (data.data && Array.isArray(data.data)) {
			profiles.value = data.data
				.filter((profile: Profile) => profile.userId !== currentUser.value?.id)
				.slice(0, 4); // Get only the latest 4 profiles
		}
	} catch (error) {
		console.error('Error loading profiles:', error);
	} finally {
		loading.value = false;
	}
};

// Load favorites
const loadFavorites = async (): Promise<void> => {
	try {
		if (currentUser.value?.id) {
			const response = await getUserFavorites(currentUser.value.id);
			if (response.data && Array.isArray(response.data)) {
				favorites.value = response.data.map((fav: any) => fav.profileId || fav.profile_id);
			}
		}
	} catch (error) {
		console.error('Error loading favorites:', error);
	}
};

// Perform search
const performSearch = async (searchParams: ProfileSearchParams): Promise<void> => {
	loading.value = true;
	isSearching.value = true;

	try {
		const data = await searchProfiles(searchParams);
		// Filter out current user's profiles
		if (data.data && Array.isArray(data.data)) {
			profiles.value = data.data.filter((profile: Profile) => profile.userId !== currentUser.value?.id);
		}
	} catch (error) {
		console.error('Error searching profiles:', error);
	} finally {
		loading.value = false;
	}
};
</script>

<template>
	<div class="home">
		<div class="mt-4">
			<h1 class="mb-4">
				Welcome to JamDate
			</h1>

			<div v-if="hasProfiles">
				<SearchForm @search="performSearch" />

				<div v-if="isSearching">
					<h2>Search Results</h2>
				</div>
				<div v-else>
					<h2>Recent Profiles</h2>
				</div>

				<div v-if="loading" class="text-center my-5">
					<output class="spinner-border text-primary">
						<span class="visually-hidden">Loading...</span>
					</output>
				</div>

				<div v-else-if="profiles.length === 0" class="alert alert-info">
					No profiles found matching your criteria.
				</div>

				<div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
					<div v-for="profile in profiles" :key="profile.id" class="col">
						<ProfileCard
							:profile="profile"
							:is-favorite="favorites.includes(profile.id)"
							@toggle-favorite="loadFavorites"
						/>
					</div>
				</div>
			</div>

			<div v-else class="alert alert-warning">
				<p>You need to complete your profile to see other users.</p>
				<router-link to="/profiles/new" class="btn btn-primary">
					Create Profile
				</router-link>
			</div>
		</div>
	</div>
</template>
