<script setup lang="ts">
import type { Favourite, Profile } from '@/services/api.types';
import ProfileCard from '@/components/ProfileCard.vue';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';

import LabelCard from '@/components/ui/LabelCard.vue';
import { addToFavorites, getProfileById, getProfileMatches, getUploadedFileUrl, getUserFavorites, removeFavouriteProfile } from '@/services/api';
import { useGlobalStore } from '@/store';
import { BabyIcon, BadgeCheckIcon, ChurchIcon, UsersIcon } from 'lucide-vue-next';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import emitter from '../eventBus';

const route = useRoute();

const profileId = Number.parseInt(route.params.id as string);
const profile = ref<Profile>();
const isFavourited = ref(false);
const favDetails = ref<Favourite>();
const loading = ref(true);
const error = ref<string>();

const favorites = ref<Favourite[]>([]);
const matches = ref<Profile[]>();

const gs = useGlobalStore();
const self = gs.user.data;

const toggleFavourite = async () => {
	if (!profile.value) return;

	try {
		if (!isFavourited.value) {
			const fav = await addToFavorites({
				profileId: profile.value!.id,
			});

			if (fav.data) favDetails.value = fav.data;
		} else if (favDetails.value) {
			await removeFavouriteProfile(favDetails.value.id);
			favDetails.value = undefined;
		}

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

const loadFavorites = async (): Promise<void> => {
	try {
		if (self?.id) {
			const response = await getUserFavorites();
			if (response.data && Array.isArray(response.data)) {
				favorites.value = response.data;
			}
		}
	} catch (error) {
		console.error('Error loading favorites:', error);
	}
};

const fetchProfile = async () => {
	loading.value = true;
	error.value = undefined;

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

const fetchMatches = async () => {
	try {
		const fetchedMatches = await getProfileMatches(profileId);
		matches.value = fetchedMatches.data;

		emitter.emit('flash', {
			message: 'Fetched matches for this profile!',
			type: 'success',
		});
	} catch (err: any) {
		console.error('Failed to fetch matches:', err);
		error.value = err.message || 'Something went wrong.';

		emitter.emit('flash', {
			message: 'Failed to fetch profile matches',
			type: 'error',
		});
	}
};

// Fetch profile data when the component is mounted
onMounted(async () => {
	await fetchProfile();
	await loadFavorites();

	const favouriteProfiles = (await getUserFavorites()).data;
	const fav = favouriteProfiles?.find(favourite => favourite.fav_profile_id === profileId);
	favDetails.value = fav;
	isFavourited.value = !!fav;
});
</script>

<template>
	<main class="p-6 tablet:p-24 space-y-12">
		<div>
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
								:src="getUploadedFileUrl(profile.user?.photo) || 'https://picsum.photos/512'"
								alt="Profile Picture"
								class="w-40 h-40 object-cover rounded-full border-4 border-muted shadow-md"
							>
						</div>
						<p class="text-lg font-bold">
							About {{ profile?.user?.name }}
						</p>
						<div class="space-y-2 flex flex-wrap gap-1">
							<Badge v-if="profile.political" class="h-8 hover:scale-105 transition-all cursor-default">
								<BadgeCheckIcon class="!size-[16px]" />
								Political
							</Badge>
							<Badge v-if="profile.religious" class="h-8 hover:scale-105 transition-all cursor-default">
								<ChurchIcon class="!size-[16px]" />
								Religious
							</Badge>
							<Badge v-if="profile.family_oriented" class="h-8 hover:scale-105 transition-all cursor-default">
								<BabyIcon class="!size-[16px]" />
								Family Oriented
							</Badge>
						</div>
						<p>{{ profile.biography }}</p>

						<!-- Profile Info -->
						<div class="space-y-4 flex flex-wrap gap-6">
							<LabelCard label="Birth Year" :content="profile.birth_year.toString()" />
							<LabelCard label="Parish" :content="profile.parish" />
						</div>
						<div class="space-y-4 flex flex-wrap gap-6">
							<LabelCard label="Height" :content="`${profile.height.toString()} in`" />
							<LabelCard label="Sex" :content="profile.race" />
							<LabelCard label="Race" :content="profile.sex" />
						</div>
						<div class="space-y-4 flex flex-wrap gap-6">
							<LabelCard label="Favourite Cuisine" :content="profile.fav_cuisine" />
							<LabelCard label="Favourite Colour" :content="profile.fav_colour" />
							<LabelCard label="Favourite School Subject" :content="profile.fav_school_subject" />
						</div>
						<!-- Action Buttons Section -->
						<div class="flex justify-center gap-4 mt-6">
							<Button
								v-if="profile.user?.id !== self?.id"
								:variant="isFavourited ? 'destructive' : 'outline'"
								@click="toggleFavourite"
							>
								<span class="mr-2">❤️</span>
								{{ isFavourited ? 'Favourited' : 'Add to Favourites' }}
							</Button>

							<Button v-if="profile.user?.id === self?.id" @click="fetchMatches">
								<UsersIcon class="mr-2" />
								View Matches
							</Button>

							<Button variant="secondary">
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
		<div v-if="matches">
			<h1 class="text-3xl font-bold mb-3">
				Profile Matches
			</h1>
			<Card v-if="matches.length === 0" class="w-fit shadow-none border-dashed border-muted-foreground bg-muted-foreground/10">
				<CardContent>
					<p class="text-muted-foreground">
						No matches found.
					</p>
				</CardContent>
			</Card>
			<div v-else class="grid grid-cols-1 phone-big:grid-cols-2 tablet:grid-cols-3 laptop:grid-cols-4 desktop:grid-cols-5 gap-4">
				<div v-for="match in matches" :key="match.id">
					<ProfileCard
						:profile="match"
						:is-favorite="favorites.filter(f => f.fav_profile_id === profile?.id).length > 0"
						:fav-id="favorites.filter(f => f.fav_profile_id === profile?.id)[0]?.id"
						@toggle-favorite="loadFavorites"
					/>
				</div>
			</div>
		</div>
	</main>
</template>
