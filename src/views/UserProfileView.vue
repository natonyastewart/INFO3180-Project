<script setup lang="ts">
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import { getUserProfiles } from '@/services/api';
import { useGlobalStore } from '@/store';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import emitter from '../eventBus';

const router = useRouter();
const globalStorage = useGlobalStore();
const profiles = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchProfiles = async () => {
	loading.value = true;
	error.value = null;

	try {
		const response = await getUserProfiles(globalStorage.user.data!.id!);
		profiles.value = response.data ?? [];

		loading.value = false;
	} catch (err: any) {
		console.error('Failed to fetch user profiles:', err);
		error.value = err.message || 'Failed to load profiles';
		loading.value = false;

		emitter.emit('flash', {
			message: 'Failed to load profiles',
			type: 'error',
		});
	}
};

const goToProfile = (id: string) => {
	router.push({ name: 'ProfileDetails', params: { profile_id: id } });
};

const createNewProfile = () => {
	router.push({ name: 'NewProfile' });
};

onMounted(fetchProfiles);
</script>

<template>
	<main>
		<div class="mt-5">
			<Card class="max-w-5xl mx-auto">
				<CardHeader class="flex justify-between items-center">
					<h1 class="text-xl font-bold">
						My Profiles
					</h1>
					<Button @click="createNewProfile">
						Create New Profile
					</Button>
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

					<div v-else-if="profiles.length" class="grid md:grid-cols-2 gap-6">
						<Card
							v-for="profile in profiles"
							:key="profile.id"
							class="cursor-pointer hover:shadow-lg transition"
							@click="goToProfile(profile.id)"
						>
							<CardContent class="p-4">
								<div class="flex items-center gap-4">
									<!-- Profile Image -->
									<img
										:src="profile.photo || 'https://via.placeholder.com/100'"
										alt="Profile picture"
										class="w-20 h-20 rounded-full object-cover border"
									>
									<div>
										<h2 class="text-xl font-semibold">
											{{ profile.name }}
										</h2>
										<p class="text-muted-foreground text-sm">
											{{ profile.description }}
										</p>
									</div>
								</div>
								<div class="mt-4">
									<p><strong>Sex:</strong> {{ profile.sex }}</p>
									<p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
									<p><strong>Height:</strong> {{ profile.height }} in</p>
								</div>
							</CardContent>
						</Card>
					</div>

					<div v-else class="text-center text-muted-foreground p-8">
						<p class="mb-4">
							No profiles found.
						</p>
						<Button @click="createNewProfile">
							Create Your First Profile
						</Button>
					</div>
				</CardContent>
			</Card>
		</div>
	</main>
</template>
