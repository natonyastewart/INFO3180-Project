<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { HeartIcon } from 'lucide-vue-next';
import { ref } from 'vue';
import { addToFavorites } from '../services/api';

const props = defineProps<{
	profileId: number;
	isFavorite: boolean;
}>();

const emit = defineEmits(['toggle']);
const isLoading = ref(false);

async function toggleFavorite() {
	try {
		isLoading.value = true;
		await addToFavorites({ userId: props.profileId });
		emit('toggle');
	} catch (error) {
		console.error('Error toggling favorite:', error);
	} finally {
		isLoading.value = false;
	}
}
</script>

<template>
	<Button
		variant="outline"
		size="icon"
		class="favorite-btn" :class="[
			{ 'bg-destructive/10 hover:bg-destructive/20': isFavorite },
		]"
		:disabled="isLoading"
		@click.prevent="toggleFavorite"
	>
		<HeartIcon
			class="h-4 w-4" :class="[
				isFavorite ? 'fill-destructive text-destructive' : 'fill-none text-destructive',
			]"
		/>
		<span class="sr-only">{{ isFavorite ? 'Remove from favorites' : 'Add to favorites' }}</span>
	</Button>
</template>
