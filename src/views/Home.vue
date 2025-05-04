<script setup lang="ts">
import type { Profile, ProfileSearchParams } from '../services/api.types';
import type { UserData } from '../store';

import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { onMounted, ref } from 'vue';
import ProfileCard from '../components/ProfileCard.vue';
import SearchForm from '../components/SearchForm.vue';
import { getProfiles, getUserFavorites, searchProfiles } from '../services/api';
import { getCurrentUser } from '../services/auth';
// Define reactive state
const profiles = ref<Profile[]>([]);
const favorites = ref<number[]>([]);
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
			const response = await getProfiles();
			hasProfiles.value = response.data ? response.data.length > 0 : false;
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
		const data = await searchProfiles();
		// Filter out current user's profiles
		if (data.data && Array.isArray(data.data)) {
			profiles.value = data.data
				.filter((profile: Profile) => profile.user_id !== currentUser.value?.id)
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
			const response = await getUserFavorites();
			if (response.data && Array.isArray(response.data)) {
				favorites.value = response.data.map(fav => fav.fav_user_id);
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
		profiles.value = data.data ?? [];
	} catch (error) {
		console.error('Error searching profiles:', error);
	} finally {
		loading.value = false;
	}
};
</script>

<template>
	<div class="home">
		<div class="p-6 tablet:p-24 space-y-12">
			<h1 class="mb-4 text-5xl font-bold">
				Welcome to JamDate
			</h1>

			<div v-if="hasProfiles">
				<SearchForm @search="performSearch" />

				<div v-if="isSearching">
					<h2>Search Results</h2>
				</div>
				<div v-else>
					<h2 class="text-xl font-semibold">Recent Profiles</h2>
				</div>

				<div v-if="loading" class="text-center my-5">
					<output class="spinner-border text-primary">
						<span class="visually-hidden">Loading...</span>
					</output>
				</div>

				<div v-else-if="profiles.length === 0" class="alert alert-info">
					No profiles found matching your criteria.
				</div>

				<div v-else class="grid grid-cols-1 phone-big:grid-cols-2 tablet:grid-cols-3 laptop:grid-cols-4 desktop:grid-cols-5">
					<div v-for="profile in profiles" :key="profile.id" class="col">
						<ProfileCard
							:profile="profile"
							:is-favorite="favorites.includes(profile.user_id)"
							@toggle-favorite="loadFavorites"
						/>
					</div>
				</div>
			</div>

			<Card v-else class="p-6 w-fit shadow-none border-dashed">
				<p>You need to complete your profile to see other users.</p>
				<router-link to="/profiles/new">
					<Button>
						Create Profile
					</Button>
				</router-link>
			</Card>
		</div>
	</div>
</template>
