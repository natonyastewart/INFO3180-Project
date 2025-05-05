<script setup lang="ts">
import type { Profile } from '@/services/api.types';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import { getUploadedFileUrl, getUserFavorites } from '@/services/api';
import { onMounted, ref } from 'vue';
import emitter from '../eventBus';

const favourites = ref<Profile[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchFavourites = async () => {
	loading.value = true;
	error.value = null;

	try {
		favourites.value = (await getUserFavorites()).data?.map(fav => fav.profile).filter(x => !!x) ?? [];
	} catch (err: any) {
		console.error('Failed to load favourites:', err);
		error.value = err.message || 'Failed to load favourites';

		emitter.emit('flash', {
			message: 'Failed to load favourites',
			type: 'error',
		});
	} finally {
		loading.value = false;
	}
};

onMounted(fetchFavourites);
</script>

<template>
	<main>
		<div class="mt-5">
			<Card class="max-w-5xl mx-auto">
				<CardHeader class="text-xl font-bold text-center">
					Your Favourite Profiles
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

					<div v-else-if="favourites.length" class="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
						<Card
							v-for="profile in favourites"
							:key="profile.id"
							class="bg-background hover:shadow-md transition p-0"
						>
							<CardContent class="p-4">
								<img
									:src="getUploadedFileUrl(profile.user?.photo) || 'https://picsum.photos/512'"
									alt="Profile Picture"
									class="w-full h-48 object-cover rounded-md mb-4"
								>

								<h2 class="text-xl font-semibold mb-2">
									{{ profile.user?.name }}
								</h2>
								<p class="text-sm text-muted-foreground mb-1">
									<strong>Sex:</strong> {{ profile.sex }}
								</p>
								<p class="text-sm text-muted-foreground mb-1">
									<strong>Race:</strong> {{ profile.race }}
								</p>
								<p class="text-sm text-muted-foreground mb-1">
									<strong>Parish:</strong> {{ profile.parish }}
								</p>

								<router-link
									:to="`/profiles/${profile.id}`"
									class="inline-block mt-4 text-primary hover:underline font-medium"
								>
									View More Details →
								</router-link>
							</CardContent>
						</Card>
					</div>

					<div v-else class="text-center text-muted-foreground text-lg p-8">
						No favourites found.
					</div>
				</CardContent>
			</Card>
		</div>
	</main>
</template>
