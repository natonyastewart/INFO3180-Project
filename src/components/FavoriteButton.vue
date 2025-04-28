<template>
	<button class="btn btn-outline-danger favorite-btn" @click.prevent="toggleFavorite" :class="{ active: isFavorite }">
		<i class="fas fa-heart" :class="{ 'text-danger': isFavorite }"></i>
	</button>
</template>

<script lang="ts">
import { addToFavorites } from '../services/api';

export default {
	name: 'FavoriteButton',
	props: {
		profileId: {
			type: Number,
			required: true,
		},
		isFavorite: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		async toggleFavorite() {
			try {
				await addToFavorites(this.profileId);
				this.$emit('toggle');
			} catch (error) {
				console.error('Error toggling favorite:', error);
			}
		},
	},
};
</script>

<style scoped>
.favorite-btn.active {
	background-color: #ffebee;
}
</style>
