<script setup lang="ts">
import type { Favourite, Profile, ProfileSearchParams } from '../services/api.types';
import type { UserData } from '../store';

import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { onMounted, ref } from 'vue';
import ProfileCard from '../components/ProfileCard.vue';
import SearchForm from '../components/SearchForm.vue';
import { getProfiles, getUserFavorites, searchProfiles } from '../services/api';
import { getCurrentUser } from '../services/auth';

const profiles = ref<Profile[]>([]);
const favorites = ref<Favourite[]>([]);
const loading = ref<boolean>(true);
const isSearching = ref<boolean>(false);
const hasProfiles = ref<boolean>(false);
const currentUser = ref<UserData | null>(null);

const checkUserProfile = async (): Promise<void> => {
	try {
		if (currentUser.value?.id) {
			const response = await getProfiles();
			hasProfiles.value = response.data ? response.data.length > 0 : false;
		}
	} catch (error) {
		console.error('Error checking user profile:', error);
		hasProfiles.value = false;
	}
};

const loadProfiles = async (): Promise<void> => {
	loading.value = true;
	try {
		const data = await searchProfiles({ limit: 4 });
		if (data.data && Array.isArray(data.data)) {
			profiles.value = data.data
				.filter((profile: Profile) => profile.user_id !== currentUser.value?.id);
		}
	} catch (error) {
		console.error('Error loading profiles:', error);
	} finally {
		loading.value = false;
	}
};

const loadFavorites = async (): Promise<void> => {
	try {
		if (currentUser.value?.id) {
			const response = await getUserFavorites();
			if (response.data && Array.isArray(response.data)) {
				favorites.value = response.data;
			}
		}
	} catch (error) {
		console.error('Error loading favorites:', error);
	}
};

const performSearch = async (searchParams: ProfileSearchParams): Promise<void> => {
	loading.value = true;
	isSearching.value = true;

	try {
		const data = await searchProfiles(searchParams);
		profiles.value = data.data ?? [];
	} catch (error) {
		console.error('Error searching profiles:', error);
	} finally {
		loading.value = false;
	}
};

onMounted(async () => {
	currentUser.value = getCurrentUser();
	await checkUserProfile();

	if (hasProfiles.value) {
		await Promise.all([loadProfiles(), loadFavorites()]);
	}
});
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
					<h2 class="text-2xl font-bold mb-3">
						Search Results
					</h2>
				</div>
				<div v-else>
					<h2 class="text-xl font-semibold">
						Recent Profiles
					</h2>
				</div>

				<div v-if="loading" class="text-center my-5">
					<output class="spinner-border text-primary">
						<span class="visually-hidden">Loading...</span>
					</output>
				</div>

				<Card v-else-if="profiles.length === 0" class="shadow-none border-dashed border-destructive bg-destructive/10 p-6 w-fit">
					No profiles found matching your criteria.
				</Card>

				<div v-else class="grid grid-cols-1 phone-big:grid-cols-2 tablet:grid-cols-3 laptop:grid-cols-4 desktop:grid-cols-5 gap-4">
					<div v-for="profile in profiles" :key="profile.id" class="col">
						<ProfileCard
							:profile="profile"
							:is-favorite="favorites.filter(f => f.fav_profile_id === profile.id).length > 0"
							:fav-id="favorites.filter(f => f.fav_profile_id === profile.id)[0]?.id"
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
