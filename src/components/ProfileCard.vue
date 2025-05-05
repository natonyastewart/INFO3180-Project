<script setup lang="ts">
import type { Profile } from '@/services/api.types';
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardFooter from '@/components/ui/card/CardFooter.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import { getUploadedFileUrl } from '@/services/api';
import { computed } from 'vue';
import FavoriteButton from './FavoriteButton.vue';

const props = defineProps<{
	profile: Profile;
	isFavorite: boolean;
	favId?: number;
}>();

const emit = defineEmits(['toggleFavorite']);

const calculateAge = (birthYear: number) => {
	const currentYear = new Date().getFullYear();
	return currentYear - birthYear;
};

const profileImage = computed(() => getUploadedFileUrl(props.profile.user?.photo) || 'https://picsum.photos/512');
</script>

<template>
	<Card class="h-full overflow-hidden pt-0">
		<div class="aspect-square w-full overflow-hidden">
			<img
				:src="profileImage"
				:alt="`${profile.user?.name}'s profile`"
				class="h-full w-full object-cover transition-all hover:scale-105"
			>
		</div>

		<CardHeader class="pb-2">
			<h3 class="text-lg font-semibold">
				{{ profile.user?.name ?? 'Unknown User' }}
			</h3>
		</CardHeader>

		<CardContent class="pb-2">
			<div class="space-y-1 text-sm">
				<p><span class="font-medium">Parish:</span> {{ profile.parish }}</p>
				<p><span class="font-medium">Age:</span> {{ calculateAge(profile.birth_year) }}</p>
				<p><span class="font-medium">Sex:</span> {{ profile.sex }}</p>
			</div>
		</CardContent>

		<CardFooter class="flex justify-between pt-2">
			<Button as-child variant="default" size="sm">
				<router-link :to="`/profiles/${profile.id}`">
					View details
				</router-link>
			</Button>

			<FavoriteButton
				:profile-id="profile.id"
				:is-favorite="isFavorite"
				:fav-id="favId"
				@toggle="emit('toggleFavorite')"
			/>
		</CardFooter>
	</Card>
</template>
