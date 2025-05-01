<script setup lang="ts">
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import { addToFavorites, getProfileById } from '@/services/api';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import emitter from '../eventBus';

const route = useRoute();
const profileId = route.params.id as string;
const profile = ref<any>(null);
const message = ref('');
const isFavourited = ref(false);
const loading = ref(true);
const error = ref<string | null>(null);

const toggleFavourite = async () => {
	try {
		await addToFavorites(profile.value.id);
		isFavourited.value = !isFavourited.value;

		const messageText = isFavourited.value ? 'Profile added to your favourites!' : 'Profile removed from your favourites';

		emitter.emit('flash', {
			message: messageText,
			type: isFavourited.value ? 'success' : 'info',
		});
	} catch (err: any) {
		console.error('Failed to favourite profile:', err);
		error.value = err.message || 'Something went wrong.';

		emitter.emit('flash', {
			message: 'Failed to update favourites',
			type: 'error',
		});
	}
};

const fetchProfile = async () => {
	loading.value = true;
	error.value = null;

	try {
		const response = await getProfileById(profileId);
		profile.value = response.data;

		loading.value = false;
	} catch (err: any) {
		console.error('Failed to load profile:', err);
		error.value = err.message || 'Failed to load profile';
		loading.value = false;

		emitter.emit('flash', {
			message: 'Failed to load profile',
			type: 'error',
		});
	}
};

// Fetch profile data when the component is mounted
onMounted(() => {
	fetchProfile();
});
</script>

<template>
	<main>
		<div class="mt-5">
			<Card class="max-w-3xl mx-auto">
				<CardHeader class="text-xl font-bold text-center">
					Profile Details
				</CardHeader>
				<CardContent>
					<div v-if="error" class="p-4 border border-destructive rounded-lg bg-destructive/10 text-destructive mb-4">
						{{ error }}
					</div>

					<div v-if="loading" class="text-center p-8">
						<div class="spinner-border" role="status">
							<span class="visually-hidden">Loading...</span>
						</div>
					</div>

					<div v-else-if="profile" class="space-y-6">
						<!-- Profile Image -->
						<div class="flex justify-center">
							<img
								:src="profile.photo || 'https://via.placeholder.com/150'"
								alt="Profile Picture"
								class="w-40 h-40 object-cover rounded-full border-4 border-muted shadow-md"
							>
						</div>

						<!-- Profile Info -->
						<div class="space-y-4">
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
						<div class="flex justify-center gap-4 mt-6">
							<Button
								:variant="isFavourited ? 'destructive' : 'outline'"
								class="flex items-center"
								@click="toggleFavourite"
							>
								<span class="mr-2">❤️</span>
								{{ isFavourited ? 'Favourited' : 'Add to Favourites' }}
							</Button>

							<Button variant="secondary" class="flex items-center">
								<span class="mr-2">📧</span>
								Email Profile
							</Button>
						</div>
					</div>

					<div v-else class="text-center text-muted-foreground p-8">
						Profile not found.
					</div>
				</CardContent>
			</Card>
		</div>
	</main>
</template>
