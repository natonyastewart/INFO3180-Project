<script lang="ts">
import FavoriteButton from './FavoriteButton.vue';

export default {
	name: 'ProfileCard',
	components: {
		FavoriteButton,
	},
	props: {
		profile: {
			type: Object,
			required: true,
		},
		isFavorite: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		calculateAge(birthYear: number) {
			const currentYear = new Date().getFullYear();
			return currentYear - birthYear;
		},
	},
};
</script>

<template>
	<div class="card h-100">
		<img :src="profile.photo || '/default-profile.jpg'" class="card-img-top" alt="Profile">
		<div class="card-body">
			<h5 class="card-title">
				{{ profile.name }}
			</h5>
			<p class="card-text">
				<strong>Parish:</strong> {{ profile.parish }}<br>
				<strong>Age:</strong> {{ calculateAge(profile.birth_year) }}<br>
				<strong>Sex:</strong> {{ profile.sex }}
			</p>
			<div class="d-flex justify-content-between">
				<router-link :to="`/profiles/${profile.id}`" class="btn btn-primary">
					View more details
				</router-link>
				<FavoriteButton
					:profile-id="profile.id"
					:is-favorite="isFavorite"
					@toggle="$emit('toggleFavorite')"
				/>
			</div>
		</div>
	</div>
</template>
